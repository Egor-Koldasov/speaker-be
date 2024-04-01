"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const fastify_1 = require("fastify");
const app = (0, fastify_1.default)({ logger: true });
app.listen({ port: 9000 }, () => console.info("api listening at http://localhost:9000"));
