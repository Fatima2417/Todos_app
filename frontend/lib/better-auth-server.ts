// lib/better-auth-server.ts
// Server-side Better Auth configuration
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    provider: "sqlite", // Using SQLite for simplicity, but you can switch to PostgreSQL
    url: process.env.DATABASE_URL || "./db.sqlite",
  },
  secret: process.env.BETTER_AUTH_SECRET || "dyOjElLwSUu3U5XyaPw1Z304H6JdCnBL",
  emailAndPassword: {
    enabled: true,
  },
  socialProviders: {},
});