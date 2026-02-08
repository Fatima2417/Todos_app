// This API route handles Better Auth server-side functionality
import { auth } from '../../../../lib/better-auth-server';
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);