"use client";

import {
  EmailPasswordSignUpFormDataSchema,
  EmailPasswordSignUpFormData,
} from "@/models/email-password-sign-up-data";
import {
  SignUpFormDataSchema,
  SignUpFormData,
} from "@/models/sign-up-form-data";

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
import axios from "axios";

export function SignUpForm() {
  const form = useForm<SignUpFormData>({
    resolver: zodResolver(SignUpFormDataSchema),
    defaultValues: {
      displayName: "",
      email: "",
      password: "",
      confirmedPassword: "",
    },
  });

  const handleSumbitFormData = (data: SignUpFormData) => {
    // form.reset();
    const emailPasswordData = EmailPasswordSignUpFormDataSchema.parse(data);
    const response = axios.post("/api/auth/sign-up", emailPasswordData);
    console.debug(response);
  };

  return (
    <Card className="w-[25rem]">
      <CardHeader>Sign Up</CardHeader>
      <CardContent className="flex flex-col gap-4">
        <Form {...form}>
          <form
            onSubmit={form.handleSubmit(handleSumbitFormData)}
            className="flex flex-col gap-4"
          >
            <FormField
              control={form.control}
              name="displayName"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input {...field} placeholder="Name" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

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

            <FormField
              control={form.control}
              name="confirmedPassword"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirm Password</FormLabel>
                  <FormControl>
                    <PasswordInput {...field} placeholder="Confirm Password" />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <Button type={"submit"}>Sign Up</Button>
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
        <p className="text-muted-foreground">Already have an account?</p>
        <Link href="#" className="text-foreground underline">
          Sign In
        </Link>
      </CardFooter>
    </Card>
  );
}
