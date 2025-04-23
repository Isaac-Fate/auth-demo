import { z } from "zod";

export const EmailPasswordSignUpFormDataSchema = z.object({
  displayName: z.string().min(1),
  email: z.string().email(),
  password: z.string().min(8),
});

export type EmailPasswordSignUpFormData = z.infer<
  typeof EmailPasswordSignUpFormDataSchema
>;
