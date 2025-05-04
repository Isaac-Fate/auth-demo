"use server";

import { cookies } from "next/headers";
import { UserSchema, User } from "@/models";

export async function getCurrentUser(): Promise<User | null> {
  // Get the cookie store
  const cookieStore = await cookies();

  // Get the access token
  const accessToken = cookieStore.get("accessToken")?.value;

  if (!accessToken) {
    return null;
  }

  const response = await fetch(
    `${process.env.BACKEND_API_BASE_URL}/auth/current-user`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    },
  );

  try {
    const user = UserSchema.parse(await response.json());
    return user;
  } catch (error) {
    return null;
  }
}
