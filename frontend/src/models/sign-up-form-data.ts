import { z } from "zod";

export const SignUpFormDataSchema = z
  .object({
    displayName: z.string().min(1),
    email: z.string().email(),
    password: z.string().min(8),
    confirmedPassword: z.string().min(8),
  })
  .refine((data) => data.password === data.confirmedPassword, {
    message: "Passwords do not match",
    path: ["confirmedPassword"],
  });

export type SignUpFormData = z.infer<typeof SignUpFormDataSchema>;
