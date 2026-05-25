import type { FastifyInstance } from "fastify";
import fp from "fastify-plugin";
import { RateLimitStore } from "../utils/rate-limit-store";

interface RateLimitOptions {
  max?: number;
  window?: number;
}

const DEFAULT_MAX = 100;
export default fp(async function rateLimitPlugin(fastify) {
  const store = new RateLimitStore();

  fastify.addHook("onRequest", (request, reply, done) => {
    const allowed = store.check(request.ip);
    if (!allowed) {
      reply.code(429).send({ error: "Too Many Requests" });
    }
    done();
  });
});
