# React Native / Expo (iOS, Android, Android TV / tvOS via react-native-tvos)

## Conventions to detect and respect
- Expo vs bare, navigation (`@react-navigation/*` or Expo Router), styling (StyleSheet, NativeWind/Tailwind, Tamagui, Restyle, styled-components), theme/token module, `react-native-tvos` fork or `@react-native-tvos/config-tv`, image library (`expo-image`, FastImage), video (`react-native-video`, `expo-video`), safe-area (`react-native-safe-area-context`), reanimated/gesture-handler.

## Mobile rules
- Navigation: bottom tabs (`tabBarLabel` visible, `accessibilityRole`), native stack with platform transitions, bottom sheets (`@gorhom/bottom-sheet`) for secondary tasks; respect Android back and iOS swipe back.
- Tokens: a theme module with semantic roles for light/dark (`useColorScheme`); no literal colours in components; validate with `tokens.py`.
- Text: `allowFontScaling` on (default), `maxFontSizeMultiplier` only where layout truly cannot grow, system fonts or bundled fonts via `expo-font`.
- Lists: `FlatList`/`FlashList` with `keyExtractor`, `getItemLayout` when fixed heights, `initialNumToRender` small, `removeClippedSubviews`; swipe actions via gesture-handler `Swipeable` with a visible menu equivalent.
- Forms: `TextInput` `keyboardType`, `returnKeyType`, `autoComplete`/`textContentType`, `KeyboardAvoidingView`/keyboard-controller, labels as `Text` + `accessibilityLabel`.
- Accessibility: `accessibilityRole/Label/State/Hint`, `accessible` grouping for cards, `AccessibilityInfo.announceForAccessibility`, `isReduceMotionEnabled`; `importantForAccessibility="no"` for decorative.
- Motion: Reanimated springs/timing on the UI thread; shared element transitions where supported; respect reduce motion.
- Insets: `SafeAreaView`/`useSafeAreaInsets` for bottom actions and headers; edge-to-edge on Android.

## TV rules (react-native-tvos)
- Focus: `Pressable`/`TouchableOpacity` are focusable; `hasTVPreferredFocus` for initial focus (Play on detail); `TVFocusGuideView` (`destinations`, `autoFocus`, `trapFocusLeft/Right/Up/Down`) to route LEFT from rails into side navigation and to keep focus memory per rail; `nextFocusUp/Down/Left/Right` for explicit paths (EPG); `onFocus/onBlur` to drive scale (Reanimated) + border/glow; `TVEventHandler`/`useTVEventHandler` for `playPause`, `menu`/back, `select`.
- Rails: horizontal `FlatList` with `getItemLayout`, `contentContainerStyle` padding for 5% safe margins, focused item scrolled to a pivot via `scrollToIndex({viewPosition: 0.2})`; images sized to cards; lazy rails.
- No touch/hover assumptions; `Platform.isTV` branches for layout scale (type ≥24 at 1080p), dark-first theme, transport controls with media keys, `BackHandler` unwinding layers.
- Performance: avoid re-rendering whole rails on focus (memoised cards, focus state local), cap backdrop resolution, test on a low-end box.

## Verification
iOS/Android simulators for mobile (font scale, VoiceOver/TalkBack); Android TV emulator with `adb shell input keyevent KEYCODE_DPAD_*` and screenshots; tvOS simulator with remote emulation.
