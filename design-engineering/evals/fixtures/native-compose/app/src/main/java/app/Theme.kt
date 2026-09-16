package app
import androidx.compose.material3.*
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
val Manrope = FontFamily(Font(R.font.manrope_regular, FontWeight.Normal), Font(R.font.manrope_semibold, FontWeight.SemiBold))
val AppTypography = Typography(bodyLarge = TextStyle(fontFamily = Manrope, fontSize = 16.sp), titleLarge = TextStyle(fontFamily = Manrope, fontWeight = FontWeight.SemiBold, fontSize = 22.sp))
val LightColors = lightColorScheme(surface = Color(0xFFFFFFFF), background = Color(0xFFF7F7F8), primary = Color(0xFF1F5EFF))
val DarkColors = darkColorScheme(surface = Color(0xFF121316), background = Color(0xFF0B0C0E))
@Composable fun AppTheme(dark: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
  MaterialTheme(colorScheme = if (dark) DarkColors else LightColors, typography = AppTypography, shapes = Shapes(medium = RoundedCornerShape(12.dp)), content = content)
}
