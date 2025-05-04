import { User } from "@/models";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Separator } from "@/components/ui/separator";
import { useAuthContext } from "@/contexts/auth-context";
import { LogOutIcon, UserIcon } from "lucide-react";
import { Button } from "./ui/button";

export function UserProfile() {
  const { user, signOut } = useAuthContext();

  return (
    <Card className="w-100">
      <CardHeader>
        <CardTitle>User Profile</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <section className="flex flex-col gap-4">
          <div className="flex flex-row justify-between gap-4">
            <p>Avatar</p>
            <Avatar className="">
              <AvatarImage src={user?.avatarUrl || undefined} />
              <AvatarFallback>
                {user === null ? (
                  <UserIcon className="text-muted-foreground size-5" />
                ) : (
                  user.displayName.slice(0, 2).toUpperCase()
                )}
              </AvatarFallback>
            </Avatar>
          </div>

          <div className="flex flex-row justify-between gap-4">
            <p>Display Name</p>
            <div className="flex flex-col">
              <p>{user?.displayName}</p>
            </div>
          </div>

          <div className="flex flex-row justify-between gap-4">
            <p>Email</p>
            <div className="flex flex-col">
              <p>{user?.email}</p>
            </div>
          </div>
        </section>

        <Separator />

        <section className="flex flex-col gap-4">
          <p>Accounts</p>

          <div className="flex flex-row justify-between gap-4">
            <p>Email</p>
            <div className="flex flex-col">
              <p>{user?.email}</p>
            </div>
          </div>
        </section>
      </CardContent>

      <CardFooter>
        <div
          onClick={() => {
            signOut();
          }}
          className="group flex flex-row items-center gap-2 select-none hover:cursor-pointer"
        >
          <p className="text-muted-foreground">Sign Out</p>
          <LogOutIcon
            className="-me-1 opacity-60 transition-transform group-hover:translate-x-0.5"
            size={16}
            aria-hidden="true"
          />
        </div>
      </CardFooter>
    </Card>
  );
}
