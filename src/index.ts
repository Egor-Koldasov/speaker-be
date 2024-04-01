import fastify from "fastify";

const app = fastify({ logger: true });

app.listen({ port: 9000 }, () =>
  console.info("api listening at http://localhost:9000")
);
