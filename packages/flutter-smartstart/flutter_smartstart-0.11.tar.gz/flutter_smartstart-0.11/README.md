# Flutter SmartStart

Flutter SmartStart is a CLI tool to create and customize Flutter projects with a clean code folder structure. It helps you quickly set up a new Flutter project with a standardized and maintainable architecture.

## Features

- Interactive prompts for project name, package name, and package version
- Automatically adds specified packages to `pubspec.yaml`
- Creates a [README.md](http://readme.md/) file with project information
- Ensures a clean and organized code structure

## Installation

You can install Flutter SmartStart using `pip`:

```
pip install flutter-smartstart

```

## Usage

### Create a New Flutter Project

Run the `flutter-smartstart cp` command and follow the prompts to create a new Flutter project:

```
flutter-smartstart cp

```

You will be prompted to enter the project name:

```
Project name please ? : my_flutter_app

```

After providing the input, Flutter SmartStart will create the Flutter project and set up the initial folder structure.

### Add Folder Structure to Existing Project

Run the `flutter-smartstart afs` command and follow the prompts to add a clean code folder structure to an existing Flutter project:

```
flutter-smartstart afs

```

You will be prompted to enter the project name and the feature name:

```
Project name please ? : my_flutter_app
Feature name please ? : user_authentication

```

After providing the inputs, Flutter SmartStart will add the specified folder structure to the project.

### Add a Package to an Existing Project

Run the `flutter-smartstart apkg` command and follow the prompts to add a package to an existing Flutter project:

```
flutter-smartstart apkg

```

You will be prompted to enter the project name and the package name:

```
Project name please ? : my_flutter_app
Package name please ? : provider

```

After providing the inputs, Flutter SmartStart will add the specified package to the project's `pubspec.yaml`.

### Project Structure

The generated Flutter project will have the following structure:

```
my_flutter_app/
├── android/
├── ios/
├── lib/
│   ├── core/
│   │   ├── connection/
│   │   ├── constants/
│   │   ├── errors/
│   ├── config/
│   │   ├── routes/
│   │   ├── themes/
│   ├── features/
│   │   ├── feature_name/
│   │   │   ├── data/
│   │   │   │   ├── datasources/
│   │   │   │   ├── models/
│   │   │   │   ├── repositories/
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   ├── repositories/
│   │   │   │   ├── usecases/
│   │   │   ├── presentation/
│   │   │   │   ├── pages/
│   │   │   │   ├── widgets/
│   │   │   │   ├── providers/
│   ├── main.dart
├── assets/
│   ├── images/
│   ├── fonts/
├── test/
├── pubspec.yaml
├── README.md
└── ...


```

## Contact

If you have any questions or feedback, feel free to open an issue or reach out to the project maintainer:

Name: Kapil Bhandari

Email: [iam.bkpl03@gmail.com](iam.bkpl03@gmail.com)

