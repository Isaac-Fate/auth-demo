"use server";

import { cookies } from "next/headers";
import { SignInFormData } from "@/models";

export async function signIn(signInFormData: SignInFormData) {
  // Get the cookie store
  const cookieStore = await cookies();

  const response = await fetch(
    `${process.env.BACKEND_API_BASE_URL}/auth/sign-in`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(signInFormData),
    },
  );

  const data = (await response.json()) as {
    accessToken: string;
  };

  // Set the access token
  cookieStore.set("accessToken", data.accessToken, {
    httpOnly: true,
    secure: true,
    sameSite: true,
  });
}
