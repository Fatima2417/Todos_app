// Placeholder file to maintain compatibility with existing imports
// This will be removed once all references are updated
export const betterAuth = {
  signUp: {
    email: async () => ({ error: { message: "Simple auth system in use" } })
  },
  signIn: {
    email: async () => ({ error: { message: "Simple auth system in use" } })
  },
  getSession: async () => null,
  signOut: async () => {}
};