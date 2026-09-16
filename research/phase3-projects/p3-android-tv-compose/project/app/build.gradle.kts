plugins { id("com.android.application"); id("org.jetbrains.kotlin.android") }
android {
    namespace = "com.example.tv"
    compileSdk = 35
    defaultConfig { applicationId = "com.example.tv"; minSdk = 24; targetSdk = 35 }
    buildFeatures { compose = true }
}
dependencies {
    implementation("androidx.activity:activity-compose:1.10.1")
    implementation("androidx.compose.ui:ui:1.8.0")
    implementation("androidx.compose.foundation:foundation:1.8.0")   // LazyRow/LazyColumn with focus-aware scrolling (≥1.7); TvLazyRow is deprecated
    implementation("androidx.compose.material:material-icons-core:1.7.8")
    implementation("androidx.tv:tv-material:1.0.0")
    implementation("androidx.media3:media3-exoplayer:1.6.0")
    implementation("io.coil-kt:coil-compose:2.7.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.10.2")
}
