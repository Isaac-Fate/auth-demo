"use client";

import { useAuthContext } from "@/contexts/auth-context";

import { UserProfile } from "@/components/user-profile";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default function Home() {
  const { user } = useAuthContext();

  return (
    <div className="flex h-full flex-col items-center justify-center p-8">
      {user === null ? (
        <div className="flex flex-row gap-4">
          <Link href="/sign-in">
            <Button>Sign In</Button>
          </Link>

          <Link href="/sign-up">
            <Button variant="outline">Sign Up</Button>
          </Link>
        </div>
      ) : (
        <UserProfile />
      )}
    </div>
  );
}
