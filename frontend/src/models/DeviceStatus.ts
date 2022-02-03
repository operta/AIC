enum DeviceState {
  CHARGING = "CHARGING",
  SLEEPING = "SLEEPING",
  WORKING = "WORKING"
}

interface DeviceStatus {
  ID: number;
  available: boolean;
  battery: number;
  host: string;
  last_update: number;
  port: number;
  state: DeviceState;
}
export { DeviceStatus };
