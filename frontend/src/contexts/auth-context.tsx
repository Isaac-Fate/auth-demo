"use client";

import React, { useState, useEffect } from "react";

import { SignInFormDataSchema, SignInFormData, User } from "@/models";
import axios from "axios";
import {
  signIn as signInAction,
  getCurrentUser,
  signOut as signOutAction,
} from "@/actions";

type AuthStatus = "idle" | "loading" | "authenticated" | "unauthenticated";

interface AuthContextValue {
  status: AuthStatus;
  user: User | null;

  signIn: (signInFormData: SignInFormData) => Promise<void>;
  signOut: () => Promise<void>;
}

export const AuthContext = React.createContext<AuthContextValue | undefined>(
  undefined,
);

export function AuthContextProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [status, setStatus] = useState<AuthStatus>("idle");
  const [user, setUser] = useState<User | null>(null);

  const signIn = async (signInFormData: SignInFormData) => {
    // Update the status
    setStatus("loading");

    // Sign in and set the access token in the cookies
    await signInAction(signInFormData);

    // Get the user
    const user = await getCurrentUser();

    // Set the user
    setUser(user);

    // Update the status
    setStatus("authenticated");
  };

  const signOut = async () => {
    // Update the status
    setStatus("loading");

    // Sign out and remove the access token from the cookies
    await signOutAction();

    // Set the user to null
    setUser(null);

    // Update the status
    setStatus("idle");
  };

  useEffect(() => {
    getCurrentUser().then((user) => {
      setUser(user);
    });
  }, []);

  return (
    <AuthContext.Provider
      value={{
        status,
        user,
        signIn,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuthContext() {
  const authContext = React.useContext(AuthContext);

  if (!authContext) {
    throw new Error(
      "useAuthContext should be used within <AuthContextProvider>",
    );
  }

  return authContext;
}
