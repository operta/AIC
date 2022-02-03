module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  extends: [
    "plugin:vue/vue3-recommended",
    "plugin:prettier/recommended",
    "prettier",
    "plugin:@typescript-eslint/eslint-recommended",
    "prettier/@typescript-eslint",
    "eslint:recommended",
    "@vue/typescript/recommended",
    "@vue/prettier",
    "@vue/prettier/@typescript-eslint",
    "prettier",
  ],
  parser: "vue-eslint-parser",

  parserOptions: {
    parser: "@typescript-eslint/parser",
    project: "./tsconfig.json",
    tsconfigRootDir: "./",
    sourceType: "module",
    ecmaVersion: 2015,
    extraFileExtensions: [".vue"],
  },
  rules: {
    "vue/component-name-in-template-casing": ["error", "kebab-case"],
    // 'vue/no-deprecated-v-on-native-modifier': ['warning', 'always'],
    //'eslintvue/no-deprecated-v-bind-sync': 'off',
    "vue/v-slot-style": "off",
    "vue/no-deprecated-v-on-native-modifier": "off",
    "@typescript-eslint/camelcase": "off",
    "@typescript-eslint/naming-convention": [
      "warn",
      {
        selector: "default",
        format: ["camelCase"],
      },
      {
        selector: "variable",
        format: ["camelCase", "UPPER_CASE"],
      },
      {
        selector: "parameter",
        format: ["camelCase"],
        leadingUnderscore: "allow",
      },
      {
        selector: "memberLike",
        modifiers: ["private"],
        format: ["camelCase"],
        leadingUnderscore: "require",
      },
      {
        selector: "typeLike",
        format: ["PascalCase"],
      },
    ],
  },
  plugins: [
    "prettier",
    "eslint-plugin-import",
    "eslint-plugin-jsdoc",
    "eslint-plugin-prefer-arrow",
    "@typescript-eslint",
    "vue",
  ]
};
