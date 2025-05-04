import { z } from "zod";

export const SignInFormDataSchema = z.object({
  email: z.string().email(),
  password: z.string().min(6),
});

export type SignInFormData = z.infer<typeof SignInFormDataSchema>;
