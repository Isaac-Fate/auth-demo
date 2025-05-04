import { z } from "zod";

export const UserSchema = z.object({
  id: z.number().int().nullable().default(null),
  displayName: z.string().min(1),
  email: z.string().email(),
  avatarUrl: z.string().url().nullable().default(null),
});

export type User = z.infer<typeof UserSchema>;
