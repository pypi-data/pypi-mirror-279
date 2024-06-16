import os
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
import click
from rich.theme import Theme
from rich.console import Console

custom_theme = Theme({
  "success":"green",
  "info":"blue",
  "error":"red",
  "warning":"yellow"
})

console = Console(theme=custom_theme)

def create_flutter_app(project_name):
    try:
        subprocess.run(["flutter", "create", project_name], check=True)
        os.chdir(project_name)
        add_custom_files()
        return True

    except subprocess.CalledProcessError:
        return False


def add_custom_files():
    readme_content = ''' # Flutter App
   Welcome to the custom flutter app @iambkpl '''

    with open("README.md", 'w') as f:
       f.write(readme_content)


def add_libraries(project_name,package_name):
    try:
        os.chdir(project_name)
        subprocess.run(["flutter", "pub", "add", package_name], check=True)
        return True
    except subprocess.CalledProcessError:
      return False
    
    except Exception as e:
      console.log(e)
      return False

def create_clean_code_folder_structure(base_path, feature_name="feature_name"):
  try:
    root_folders = ["assets", "lib",]

    sub_root_folders = {
        "assets": ["images", "fonts"],
        "lib": ["core", "features", "config"],
    }

    sub_folders = {
        "lib/core": ["connection", "constants", "errors",],
        "lib/config":["routes", "themes"],
        f"lib/features/{feature_name}": ["data", "domain", "presentation"],
    }

    data_sub_folders = ["datasources", "models", "repositories"]
    domain_sub_folders = ["entities", "repositories", "usecases"]
    presentation_sub_folders = ["pages", "widgets", "providers"]

    create_folders(base_path, root_folders, sub_root_folders, sub_folders, feature_name, data_sub_folders, domain_sub_folders, presentation_sub_folders)
    create_files(base_path, feature_name)
    return True
  except Exception as e:
    return False

def create_folders(base_path, root_folders, sub_root_folders, sub_folders, feature_name, data_sub_folders, domain_sub_folders, presentation_sub_folders):



    # create root folders
    for folder in root_folders:
        os.makedirs(os.path.join(base_path, folder), exist_ok=True)

    # create sub root folders
    for root, subs in sub_root_folders.items():
        for sub in subs:
            os.makedirs(os.path.join(base_path, root, sub), exist_ok=True)

    # create sub folders
    for root, subs in sub_folders.items():
        for sub in subs:
            os.makedirs(os.path.join(base_path, root, sub), exist_ok=True)


    # create domain sub folders
    for folder in domain_sub_folders:
        path = os.path.join(base_path, "lib", "features", feature_name, "domain", folder)
        os.makedirs(path, exist_ok=True)


    # create data sub folders
    for folder in data_sub_folders:
        path = os.path.join(base_path, "lib", "features",feature_name, "data", folder)
        os.makedirs(path, exist_ok=True)

    # create presentation sub folders
    for folder in presentation_sub_folders:
        path = os.path.join(base_path, "lib","features" ,feature_name, "presentation", folder)
        os.makedirs(path, exist_ok=True)



def create_files(base_path,feature_name):

 # Define file contents
    files = {
          f"lib/core/resource/" : (
            "data_state.dart",
            f"""import '../errors/failure.dart';

abstract class DataState<T> {{
  final T? data;
  final Failure? error;

  const DataState({{
    this.data,
    this.error,
  }});
}}

class DataSuccess<T> extends DataState<T> {{
  const DataSuccess(T data) : super(data: data);
}}

class DataFailed<T> extends DataState<T> {{
  const DataFailed(Failure error) : super(error: error);
}}"""
        ),


         f"lib/core/errors/" : (
            "failure.dart",
            f"""abstract class Failure {{
  final String errorMessage;
  final Exception? exception;

  const Failure({{
    required this.errorMessage,
    this.exception,
  }});
}}

class ServerFailure extends Failure {{
  ServerFailure({{required super.errorMessage}});
}}
"""
        )
    ,

        f"lib/features/{feature_name}/domain/entities/" : (
            f"{feature_name}_entity.dart",
            f"""class {feature_name.capitalize()}Entity {{
    final String name;
    const {feature_name.capitalize()}Entity({{
        required this.name,
    }});
    }}"""
        ),

        f"lib/features/{feature_name}/domain/repositories/": (
            f"{feature_name}_repository.dart",
            f"""import '../../../../core/resource/data_state.dart';
import '../entities/{feature_name}_entity.dart';
abstract class {feature_name.capitalize()}Repository {{
Future<DataState<{feature_name.capitalize()}Entity>> get{feature_name.capitalize()}();
}}
"""
        ),

         f"lib/features/{feature_name}/domain/usecases/": (
            f"get_{feature_name}_usecase.dart",
            f"""import '../../../../core/resource/data_state.dart';
import '../entities/{feature_name}_entity.dart';
import '../repositories/{feature_name}_repository.dart';


class Get{feature_name.capitalize()}{{
final {feature_name.capitalize()}Repository _{feature_name}Repository;

Get{feature_name.capitalize()}(this._{feature_name}Repository);

Future<DataState<{feature_name.capitalize()}Entity>> call() async {{
    return await _{feature_name}Repository.get{feature_name.capitalize()}();
}}
}}
"""
        ),

         f"lib/features/{feature_name}/data/datasources/": (
            f"{feature_name}_remote_data_source.dart",
            f"""import 'package:dio/dio.dart';

import '../../../../core/constants/constants.dart';
import '../../../../core/errors/failure.dart';
import '../../datasources/models/{feature_name}_model.dart';


abstract class {feature_name.capitalize()}RemoteDataSource {{
  Future<{feature_name.capitalize()}Model> get{feature_name.capitalize()}();
}}

class {feature_name.capitalize()}RemoteDataSourceImpl implements {feature_name.capitalize()}RemoteDataSource {{
  final Dio dio;
  {feature_name.capitalize()}RemoteDataSourceImpl({{required this.dio}});

  @override
  Future<{feature_name.capitalize()}Model> get{feature_name.capitalize()}() async {{
    final response = await dio.get({feature_name.capitalize()}_URL);
    if (response.statusCode == 200) {{
      return {feature_name.capitalize()}Model.fromJson(response.data);
    }} else {{
      throw ServerFailure(errorMessage: "Error getting auth");
    }}
  }}
}}
"""
        ),

         f"lib/features/{feature_name}/datasources/models/": (
            f"{feature_name}_model.dart",
            f"""import '../../domain/entities/{feature_name}_entity.dart';

class {feature_name.capitalize()}Model extends {feature_name.capitalize()}Entity {{
  const {feature_name.capitalize()}Model({{
    required name,
  }}) : super(name: name);

  factory {feature_name.capitalize()}Model.fromJson(Map<String, dynamic> json) {{
    return {feature_name.capitalize()}Model(
      name: json["name"],
    );
  }}

  Map<String, dynamic> toJson() {{
    return {{
      "name": name,
    }};
  }}
}}

"""
        ),

         f"lib/features/{feature_name}/data/repositories/" : (
            f"{feature_name}_repository_impl.dart",
            f"""import '../../../../core/errors/failure.dart';
import '../../../../core/resource/data_state.dart';
import '../../domain/repositories/{feature_name}_repository.dart';
import '../datasources/{feature_name}_remote_data_source.dart';
import '../../datasources/models/{feature_name}_model.dart';

class {feature_name.capitalize()}RepositoryImpl implements {feature_name.capitalize()}Repository {{
  final {feature_name.capitalize()}RemoteDataSource remoteDataSource;

  {feature_name.capitalize()}RepositoryImpl({{required this.remoteDataSource}});

  @override
  Future<DataState<{feature_name.capitalize()}Model>> get{feature_name.capitalize()}() async {{
    try {{
      final {feature_name} = await remoteDataSource.get{feature_name.capitalize()}();
      return DataSuccess({feature_name});
    }} catch (e) {{
      return DataFailed(ServerFailure(errorMessage: "Failed to get {feature_name}"));
    }}
  }}
}}
"""
        ),

         f"lib/features/{feature_name}/presentation/providers/": (
            f"{feature_name}_provider.dart",
            f"""import 'package:dio/dio.dart';
import 'package:flutter/material.dart';

import '../../../../core/resource/data_state.dart';
import '../../data/datasources/{feature_name}_remote_data_source.dart';
import '../../data/repositories/{feature_name}_repository_impl.dart';
import '../../domain/entities/{feature_name}_entity.dart';
import '../../domain/usecases/get_{feature_name}_usecase.dart';

/// Provides state management for {feature_name.capitalize()} operations.
class {feature_name.capitalize()}Provider extends ChangeNotifier {{
  bool _isLoading = false;
  bool _isError = false;
  String? _errorMessage;
  String? _successMessage;

  {feature_name.capitalize()}Entity? _{feature_name}Entity;

  /// Indicates whether a {feature_name.capitalize()} operation is currently loading.
  bool get isLoading => _isLoading;

  /// Indicates whether the last {feature_name.capitalize()} operation resulted in an error.
  bool get isError => _isError;

  /// The success message from the last successful {feature_name.capitalize()} operation.
  String? get successMessage => _successMessage;

  /// The error message from the last failed {feature_name.capitalize()} operation.
  String? get errorMessage => _errorMessage;

  /// The {feature_name.capitalize()}Entity from the last successful {feature_name.capitalize()} operation.
  {feature_name.capitalize()}Entity? get {feature_name}Entity => _{feature_name}Entity;

  void _successCase(String message, [{feature_name.capitalize()}Entity? {feature_name}Entity]) {{
    _isError = false;
    _isLoading = false;
    _successMessage = message;
    _{feature_name}Entity = {feature_name}Entity;
    notifyListeners();
  }}

  void _failureCase(String message) {{
    _isError = true;
    _isLoading = false;
    _errorMessage = message;
    _{feature_name}Entity = null;
    notifyListeners();
  }}

  void eitherFailureOr{feature_name.capitalize()}() async {{
    try {{
      {feature_name.capitalize()}RepositoryImpl repositoryImpl = {feature_name.capitalize()}RepositoryImpl(
          remoteDataSource: {feature_name.capitalize()}RemoteDataSourceImpl(dio: Dio()));

      final failureOr{feature_name.capitalize()} = await Get{feature_name.capitalize()}(repositoryImpl).call();
      if (failureOr{feature_name.capitalize()} is DataSuccess) {{
        _successCase("Scuccess", failureOr{feature_name.capitalize()}.data);
      }} else {{
        _failureCase("Failed to get {feature_name}");
      }}
    }} catch (e) {{}}
  }}
}}

"""
        ),
         f"lib/core/constants/": (
            f"constants.dart",
            f"""String kName = "name";

String BASE_URL = "https://api.example.com";

// {feature_name} urls
String {feature_name.capitalize()}_URL = "$BASE_URL/{feature_name}";

"""
        ),
            f"lib/core/errors/": (
            f"failure.dart",
            f"""abstract class Failure {{
  final String errorMessage;
  final Exception? exception;

  const Failure({{
    required this.errorMessage,
    this.exception,
  }});
}}

class ServerFailure extends Failure {{
  ServerFailure({{required super.errorMessage}});
}}

"""
        ),
    }



    for path,(filename,content) in files.items():
        write_file(os.path.join(base_path, path, filename), content)


def write_file(filepath, content):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'a') as f:
        f.write(content)


class ActionValidator(Validator):
    def validate(self, document):
        if document.text not in ["1", "2", "3", "4"]:
            raise ValidationError(message="Please enter a valid number.", cursor_position=len(document.text))




@click.group()
def flutter_commands():
    """Group of commands for managing Flutter projects."""
    pass


@click.command(name="cp")
@click.option("--name","-n", type=str, prompt="Project name please ? ",help="The name of project", required=True)
# @click.argument("project_name",type=str, required=True)
def create_project(name:str):
    """Creates a new Flutter project with the given name."""
    console.log("Creating the flutter project... ", style="info")
    if create_flutter_app(name):
        console.print(f" :tada: Successfully created flutter project [bold]{name}[/] ", style="success")
    else:
      console.print(":fearful: Failed to create flutter project", style="error")

@click.command(name="afs")
@click.option("--project", "-p", prompt="Project name please ? ", help="The name of the Project", required=True)
@click.option("--feature", "-f", prompt="Feature name please ? ", help="The name of the Feature", required=True)
def add_folder_structure(project:str, feature: str):
    """Creates a clean code folder structure on the given project"""
    if create_clean_code_folder_structure(project, feature):
      console.print(":fire: successfully created clean code folder structure", style="success")
    else:
      console.print(":fearful: failed to create clean code folder structure", style="error")

@click.command(name="apkg")
@click.option("--project", "-p", prompt="Project name please ? ", help="The name of the Project", required=True)
@click.option("--package", "-pkg", prompt="Package name please ? ", help="The name of the package", required=True)
def add_package(project:str,package:str):
    """Adds a new package to the given Flutter project."""
    if add_libraries(project,package):
      console.print(f":fire: Successfully added the [bold]{package}[/]", style="success")
    else:
      console.print(f":fearful: Failed to add the [bold]{package}[/]", style="error")

flutter_commands.add_command(create_project)
flutter_commands.add_command(add_folder_structure)
flutter_commands.add_command(add_package)


if __name__ == '__main__':
    flutter_commands()




