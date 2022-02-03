import torch
from syft.workers.websocket_server import WebsocketServerWorker
criterion = torch.nn.MSELoss()

class WorkerWithModel(WebsocketServerWorker):
    @property
    def weights(self):
        return self.object_store.get_obj('weights')

    @weights.setter
    def weights(self, value):
        self.object_store.register_obj(value, 'weights')

    @property
    def bias(self):
        return self.object_store.get_obj('bias')

    @bias.setter
    def bias(self, value):
        self.object_store.register_obj(value, 'bias')

    @property
    def observations(self):
        return self.object_store.get_obj('observations')

    @observations.setter
    def observations(self, value):
        self.object_store.register_obj(value, 'observations')

    @property
    def target(self):
        return self.object_store.get_obj('target')

    @target.setter
    def target(self, value):
        self.object_store.register_obj(value, 'target')

    def load_model(self, weights, bias):
        self.object_store.register_obj(weights, 'weights')
        self.object_store.register_obj(bias, 'bias')
        return True

    def reset_gradients(self):
        if self.weights.grad is not None:
            self.weights.grad.zero_()
        if self.bias.grad is not None:
            self.bias.grad.zero_()

    def predict(self):
        predictions = self.observations @ self.weights.t() + self.bias
        return self.calculate_loss(predictions)

    def calculate_loss(self, pred):
        loss = criterion(pred.reshape(-1), self.target)
        # compute gradients
        loss.backward()
        return loss.item()

    def adjust_weights(self, learning_rate):
        with torch.no_grad():
            self.weights -= self.weights.grad * learning_rate
            self.bias -= self.bias.grad * learning_rate
            self.reset_gradients()
