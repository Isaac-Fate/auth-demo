"use client";

import {
  EmailPasswordSignUpFormDataSchema,
  EmailPasswordSignUpFormData,
} from "@/models/email-password-sign-up-data";
import { SignInFormDataSchema, SignInFormData } from "@/models";

import {
  Card,
  CardHeader,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from "@/components/ui/form";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { EmailInput } from "@/components/email-input";
import { PasswordInput } from "@/components/password-input";
import { Separator } from "@/components/ui/separator";
import { RiGithubFill, RiGoogleFill } from "@remixicon/react";
import Link from "next/link";

import { useRouter } from "next/navigation";
import { useAuthContext } from "@/contexts/auth-context";

export function SignInForm() {
  const { signIn } = useAuthContext();

  const form = useForm<SignInFormData>({
    resolver: zodResolver(SignInFormDataSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const router = useRouter();

  const handleSumbitFormData = async (data: SignInFormData) => {
    // Sign in
    await signIn(data);

    // Navigate to the home page
    router.push("/");
  };

  return (
    <Card className="w-[25rem]">
      <CardHeader>Sign In</CardHeader>
      <CardContent className="flex flex-col gap-4">
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSumbitFormData)}
            className="flex flex-col gap-4"
          >
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <EmailInput {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <PasswordInput {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button type={"submit"}>Sign In</Button>
          </form>
        </Form>

        {/* Separator */}
        <div className="flex flex-row items-center">
          <Separator className="flex-1" />
          <p className="text-muted-foreground mx-4">or</p>
          <Separator className="flex-1" />
        </div>

        {/* Social Sign In */}
        <div className="flex flex-wrap gap-4">
          {/* Google */}
          <Button
            className="flex-1"
            variant="outline"
            aria-label="Login with Google"
            size="icon"
            onClick={async () => {
              // const resposne = await axios.get("/api/auth/sign-in/google");
              // console.debug(resposne);
              window.open("/api/auth/sign-in/google", "_self");
            }}
          >
            <RiGoogleFill
              className="dark:text-primary text-[#DB4437]"
              size={16}
              aria-hidden="true"
            />
          </Button>

          {/* GitHub */}
          <Button
            className="flex-1"
            variant="outline"
            aria-label="Login with GitHub"
            size="icon"
          >
            <RiGithubFill
              className="dark:text-primary text-black"
              size={16}
              aria-hidden="true"
            />
          </Button>
        </div>
      </CardContent>

      <CardFooter className="gap-2 text-sm">
        <p className="text-muted-foreground">Don't have an account?</p>
        <Link href="/sign-up" className="text-foreground underline">
          Sign Up
        </Link>
      </CardFooter>
    </Card>
  );
}
