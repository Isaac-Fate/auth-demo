"use server";

import { cookies } from "next/headers";

export async function signOut() {
  // Get the cookie store
  const cookieStore = await cookies();

  // Remove the access token from the cookies
  cookieStore.delete("accessToken");
}
