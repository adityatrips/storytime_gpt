import React from "react";
import { Text as RNText } from "react-native";

export function Text({
  children,
  variant = "Regular",
  className,
}: {
  children: String;
  variant?:
    | "Black"
    | "Bold"
    | "ExtraBold"
    | "ExtraLight"
    | "Light"
    | "Medium"
    | "Regular"
    | "SemiBold"
    | "Thin";
  className?: String;
}) {
  return (
    <RNText className={`text-text DMSans-${variant} ${className}`}>
      {children}
    </RNText>
  );
}
