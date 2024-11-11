import { StatusBar } from "expo-status-bar";
import "../global.css";
import { Slot } from "expo-router";
import { useFonts } from "expo-font";
import { useEffect } from "react";
import * as SplashScreen from "expo-splash-screen";
import { ImageBackground } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function Layout() {
  const [loaded, error] = useFonts({
    "DMSans-Black": require("../assets/fonts/DMSans-Black.ttf"),
    "DMSans-Bold": require("../assets/fonts/DMSans-Bold.ttf"),
    "DMSans-ExtraBold": require("../assets/fonts/DMSans-ExtraBold.ttf"),
    "DMSans-ExtraLight": require("../assets/fonts/DMSans-ExtraLight.ttf"),
    "DMSans-Light": require("../assets/fonts/DMSans-Light.ttf"),
    "DMSans-Medium": require("../assets/fonts/DMSans-Medium.ttf"),
    "DMSans-Regular": require("../assets/fonts/DMSans-Regular.ttf"),
    "DMSans-SemiBold": require("../assets/fonts/DMSans-SemiBold.ttf"),
    "DMSans-Thin": require("../assets/fonts/DMSans-Thin.ttf"),
  });

  useEffect(() => {
    if (loaded || error) {
      SplashScreen.hideAsync();
    }
  }, [error, loaded]);

  if (!loaded || error) {
    return null;
  }

  return (
    <ImageBackground
      source={require("../assets/bg.png")}
      className="w-full h-full absolute top-0 left-0 bg-cover"
    >
      <StatusBar style="light" backgroundColor="#000" />
      <SafeAreaView className="px-4 flex flex-1">
        <Slot />
      </SafeAreaView>
    </ImageBackground>
  );
}
