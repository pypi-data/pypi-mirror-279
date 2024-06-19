def create_build_gradle(name):
    file_name = "build.gradle.kts"
    file_content = f'''import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {{
    id("com.android.library")
    id("kotlin-android")
    id("androidx.navigation.safeargs.kotlin")
    id("com.google.devtools.ksp")
    alias(libs.plugins.compose.compiler)
    `android-config`
}}

android {{
    namespace = "com.astropaycard.android.feature.{name}"

    flavorDimensions.add("default")

    productFlavors {{
        create("production") {{
            dimension = "default"
        }}
        create("tst") {{
            dimension = "default"
        }}
    }}

    buildTypes {{
        getByName("debug") {{
        }}

        getByName("release") {{
            proguardFile("proguard-rules.pro")
        }}
    }}
    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }}
    kotlin {{
        compilerOptions {{
            jvmTarget.set(JvmTarget.JVM_1_8)
        }}
    }}
    buildFeatures {{
        compose = true
        dataBinding = true
    }}
}}

dependencies {{
    implementation(project(":domain"))
    implementation(project(":infrastructure"))
    implementation(project(":core:common"))
    implementation(project(":core:base"))
    implementation(project(":core:design-system"))
    implementation(project(":core:ui"))

    implementation(Libs.AndroidX.Compose.modules)

    implementation(Libs.Koin.koin)
    implementation(Libs.Timber.timber)
    implementation(Libs.AndroidX.Navigation.navigationKtx)
    implementation(Libs.AndroidX.Navigation.navigationUiKtx)

    implementation(Libs.Coil.coil)

    testImplementation(Libs.Junit.junit)
    testImplementation(Libs.Mockk.mockk)
    testImplementation(Libs.Coroutines.coroutinesTest)
    testImplementation(Libs.Kluent.kluent)
    testImplementation(Libs.AndroidX.Testing.core)
    testImplementation(project(":core:base"))
}}
'''
    with open(file_name, "w") as file:
        file.write(file_content)

