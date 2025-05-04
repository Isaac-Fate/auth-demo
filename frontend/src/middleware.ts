import { NextRequest, NextResponse } from "next/server";
import { UserSchema } from "@/models";

export async function middleware(request: NextRequest) {
  // const accessToken = request.cookies.get("accessToken")?.value;
  // if (accessToken === undefined) {
  //   return NextResponse.redirect(new URL("/sign-in", request.url));
  // }
  // // Invoke the backend API to verify the access token
  // const response = await fetch(
  //   `${process.env.BACKEND_API_BASE_URL}/auth/current-user`,
  //   {
  //     method: "GET",
  //     headers: {
  //       "Content-Type": "application/json",
  //       Authorization: `Bearer ${accessToken}`,
  //     },
  //   },
  // );
  // // Get and parse the response data
  // const user = UserSchema.parse(await response.json());
  // // Pass the user data to the next middleware
  // const nextResponse = NextResponse.next();
  // nextResponse.headers.set("x-user-id", user.id?.toString() || "");
  // nextResponse.headers.set("x-user-display-name", user.displayName);
  // nextResponse.headers.set("x-user-email", user.email);
  // nextResponse.headers.set("x-user-avatar-url", user.avatarUrl || "");
  // return nextResponse;
  NextResponse.next();
}

export const config = {
  matcher: [
    // "/((?!sign-in|sign-up).*)",
    "/",
  ],
};
