
#include "clang/AST/AST.h"
#include "clang/AST/ASTConsumer.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/Frontend/ASTConsumers.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
#include "llvm/Support/raw_ostream.h"
#include <clang/AST/ASTContext.h>
#include <clang/ASTMatchers/ASTMatchFinder.h>
#include <clang/ASTMatchers/ASTMatchers.h>
#include <clang/Frontend/FrontendActions.h>
#include <fstream>
#include <llvm/ADT/STLExtras.h>

#include <map>
#include <set>
#include <sstream>
#include <string>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>


#include "CPP_Parsing.h"

using namespace clang;
using namespace clang::driver;
using namespace clang::tooling;
using namespace clang::ast_matchers;

static llvm::cl::OptionCategory ToolingSampleCategory("Tooling Sample");

using namespace std;

typedef struct {
  string name;
  string CallExpr_Loc;
  string Decl_Loc;
  string return_type;
  string decl_class;
} Call_Fun_Info;

typedef struct {
  string name;
  string type;
  string type_decl_loc;
  string if_pointer = "0";
} param;

typedef struct {
  string name;
  string type;
  string type_decl_loc;
  string decl_loc;
} g_var;

typedef struct {
  string variable_name;
  string decl_loc;
  string using_loc;
  string type;
  string type_decl_loc;
  string decl_class;
  string class_decl_loc;
} var_using;

typedef struct {
  string name;
  string loc;
} pointer_matched_func;

typedef struct {
  string name = "";
  string type;
  string loc = "";
  string call_loc;
  vector<pointer_matched_func> matched_func_list;
} pointer_func;

typedef struct {
  string function_name;           // 方法名
  string function_location;       // 声明位置
  string file_path;               // 所在文件
  vector<Call_Fun_Info> call_fun; // 调用列表
  string isbody = "1";            // 是否有函数体
  string start;                   // 起始声明位置
  string end;                     // 结束声明位置
  string return_type;             // 返回类型
  vector<param> params;           // 参数列表
  string calss;                   // 所在类
  vector<var_using> variables;    // 变量列表 局部变量+全局变量
  vector<pointer_func> call_pointer_func; // 使用函数指针
  bool if_visual = false;
  int fun_type = 0;
  int if_static = 0;
  int if_virtual = 0;
  string authority;
} Function_Constraint; // 方法

typedef struct {
  string variable_name;
  string decl_loc;
  string type;
  string type_decl_loc;
  string decl_class;
  string if_pointer = "0";
  string authority;
  string isstatic;
  string isvirtual;

} Member_variable; // 成员变量

typedef struct {
  string class_name;
  string decl_loc;
  string if_virtual = "0";
} class_info;

typedef struct {
  string class_name;
  string decl_loc;
  string start_line;
  string end_line;
  string type = "Class";
  vector<class_info> bases;
  vector<string> v_bases;
  vector<Member_variable> Member_variables;
  vector<Function_Constraint> Functions;
  vector<var_using> variables; // 变量列表 局部变量+全局变量
} class_Constraint;            // 类限制

int fun_count = 1;
Function_Constraint current_Fun;
class_Constraint current_Class;
vector<Function_Constraint> Function_list;
vector<class_Constraint> Class_list;
vector<pointer_func> pointer_func_list;
vector<g_var> global_var;

vector<string> if_loc;

string if_success = "1";

// 字符串分割函数
std::vector<std::string> split(std::string str, std::string pattern) {
  std::string::size_type pos;
  std::vector<std::string> result;
  str += pattern; // 扩展字符串以方便操作
  int size = str.size();
  for (int i = 0; i < size; i++) {
    pos = str.find(pattern, i);
    if (pos < size) {
      std::string s = str.substr(i, pos - i);
      result.push_back(s);
      i = pos + pattern.size() - 1;
    }
  }
  return result;
}

string changes(string s) {
  int pos = 0;
  while ((pos = s.find('\\', pos)) >= 0) {
    s.replace(pos, 1, "/");
    // 也可以多插入一个\来达成
    // input.insert(pos, "\\");
    pos += 1;
  }
  return s;
}

class Func_Call : public MatchFinder::MatchCallback {
public:
  // Func_Call(ASTContext* astContext) : astContext(astContext) {}
  void run(const MatchFinder::MatchResult &Result) override {
    string functionname;
    clang::LangOptions LangOpts;
    LangOpts.CPlusPlus = true;
    clang::PrintingPolicy Policy(
        LangOpts); // 指定标志为c++ 模式，用于从expr 获取类型字符串

    // 从 Result 参数中获得当前的函数声明节点，这里就使用到了匹配器 bind 的标识
    if (auto const *classDecl =
            Result.Nodes.getNodeAs<CXXRecordDecl>("CXXRecordDecl")) {
      // cout << "类声明" << endl;
      //  获取类名和类声明位置
      string class_name = classDecl->getNameAsString();
      string loc = classDecl->getSourceRange().getBegin().printToString(
          Result.Context->getSourceManager());

      string start = classDecl->getSourceRange().getBegin().printToString(
          Result.Context->getSourceManager());
      start = changes(start);
      start = split(start, ":")[2];
      string end = classDecl->getSourceRange().getEnd().printToString(
          Result.Context->getSourceManager());
      end = changes(end);
      end = split(end, ":")[2];
      bool isstruct = classDecl->isStruct();
      bool isunion = classDecl->isUnion();

      // cout << class_name << endl << loc << endl;

      int find = 0;
      class_Constraint temp_class;
      temp_class.start_line = start;
      temp_class.end_line = end;
      if (isstruct)
        temp_class.type = "Struct";
      if (isunion)
        temp_class.type = "Union";
      if (class_name != current_Class.class_name &&
          loc != current_Class.decl_loc) {
        for (int i = 0; i < Class_list.size(); i++) {
          if (class_name == Class_list[i].class_name &&
              loc == Class_list[i].decl_loc) {
            find = 1;
            temp_class = Class_list[i];
          }
        }

        // 若不存在，则新建
        if (find == 0) {
          temp_class.class_name = class_name;
          temp_class.decl_loc = loc;

          // 获得基类
          auto base_begin = classDecl->bases_begin();
          while (base_begin != classDecl->bases_end()) {
            string basetype = (*base_begin).getType().getAsString();
            string base_decl_loc =
                (*base_begin)
                    .getType()
                    ->getAsCXXRecordDecl()
                    ->getBeginLoc()
                    .printToString(Result.Context->getSourceManager());
            bool isvirtual = (*base_begin).isVirtual();
            class_info new_base;
            new_base.class_name = basetype;
            new_base.decl_loc = base_decl_loc;
            if (isvirtual == true) {
              new_base.if_virtual = 1;
            }
            temp_class.bases.push_back(new_base);
            base_begin++;
          }
        }

        // 成员变量
        auto class_fields = classDecl->fields();
        auto fields_begin = class_fields.begin();
        auto fields_end = class_fields.end();
        while (fields_begin != fields_end) {
          string field_name =
              fields_begin->getCanonicalDecl()->getNameAsString();
          string field_type =
              fields_begin->getCanonicalDecl()->getType().getAsString();
          string type_decl_loc = "";
          if (fields_begin->getCanonicalDecl()
                  ->getType()
                  ->getAsCXXRecordDecl() != NULL)
            type_decl_loc =
                fields_begin->getCanonicalDecl()
                    ->getType()
                    ->getAsCXXRecordDecl()
                    ->getBeginLoc()
                    .printToString(Result.Context->getSourceManager());
          string field_loc =
              fields_begin->getCanonicalDecl()->getBeginLoc().printToString(
                  Result.Context->getSourceManager());
          Member_variable new_field;
          new_field.variable_name = field_name;
          new_field.type = field_type;
          new_field.type_decl_loc = changes(type_decl_loc);
          new_field.decl_loc = field_loc;
          new_field.decl_class = temp_class.class_name;
          string authority;
          switch ((*fields_begin)->getAccess()) {
          case AS_public:
            authority = "public";
            break;
          case AS_protected:
            authority = "protected";
            break;
          case AS_private:
            authority = "private";
            break;

          default:
            authority = "none";
            break;
          }
          new_field.authority = authority;
          temp_class.Member_variables.push_back(new_field);
          fields_begin++;
        }

        // 方法
        auto class_methods = classDecl->methods();
        auto methods_begin = class_methods.begin();
        auto methods_end = class_methods.end();
        while (methods_begin != methods_end) {
          Function_Constraint new_method;
          string isbody = "1";
          if (!methods_begin->getCanonicalDecl()
                   ->hasBody()) // 判断函数是否有函数体，仅有一个声明的没有实现的函数停止解析
          {
            isbody = "0";
          }
          new_method.isbody = isbody;
          new_method.function_name =
              methods_begin->getCanonicalDecl()->getNameAsString();
          new_method.calss = temp_class.class_name;
          string return_type =
              methods_begin->getCanonicalDecl()->getReturnType().getAsString();

          new_method.return_type = return_type;
          string type_decl_loc = "";
          if (methods_begin->getCanonicalDecl()
                  ->getType()
                  ->getAsCXXRecordDecl() != NULL)
            type_decl_loc =
                methods_begin->getCanonicalDecl()
                    ->getReturnType()
                    ->getAsCXXRecordDecl()
                    ->getBeginLoc()
                    .printToString(Result.Context->getSourceManager());
          type_decl_loc = changes(type_decl_loc);
          new_method.return_type = type_decl_loc + "$$" + return_type;
          string method_decl_loc =
              methods_begin->getCanonicalDecl()->getBeginLoc().printToString(
                  Result.Context->getSourceManager());
          method_decl_loc = changes(method_decl_loc);
          new_method.function_location = method_decl_loc;
          new_method.file_path = split(method_decl_loc, ":")[0] + ":" +
                                 split(method_decl_loc, ":")[1];
          string start = methods_begin->getCanonicalDecl()
                             ->getSourceRange()
                             .getBegin()
                             .printToString(Result.Context->getSourceManager());
          start = changes(start);
          new_method.start = split(start, ":")[2];
          string end = methods_begin->getCanonicalDecl()
                           ->getSourceRange()
                           .getEnd()
                           .printToString(Result.Context->getSourceManager());
          end = changes(end);
          new_method.end = split(end, ":")[2];

          // 判断是不是静态函数
          int if_static = methods_begin->getCanonicalDecl()->isStatic();
          // 判断是不是虚函数
          int if_virtual = methods_begin->getCanonicalDecl()->isVirtual();
          new_method.if_static = if_static;
          new_method.if_virtual = if_virtual;

          string authority;
          switch ((*methods_begin)->getAccess()) {
          case AS_public:
            authority = "public";
            break;
          case AS_protected:
            authority = "protected";
            break;
          case AS_private:
            authority = "private";
            break;

          default:
            authority = "none";
            break;
          }
          new_method.authority = authority;

          // 获得参数列表
          auto params = methods_begin->getCanonicalDecl()->parameters();
          auto params_begin = params.begin();
          auto params_end = params.end();
          int params_size = params.size();
          for (int i = 0; i < params_size; i++) {
            string param_type = params_begin[i]->getType().getAsString();
            string type_decl_loc = "";
            if (params_begin[i]->getType()->getAsCXXRecordDecl() != NULL)
              type_decl_loc =
                  params_begin[i]
                      ->getType()
                      ->getAsCXXRecordDecl()
                      ->getBeginLoc()
                      .printToString(Result.Context->getSourceManager());
            string param_name = params_begin[i]->getNameAsString();
            param new_param;
            new_param.name = param_name;
            new_param.type = param_type;
            new_param.type_decl_loc = changes(type_decl_loc);
            new_method.params.push_back(new_param);
          }
          // 是否为虚函数
          new_method.if_visual = methods_begin->getCanonicalDecl()->isVirtual();

          // 是否为构造函数
          if (isa<CXXConstructorDecl>(methods_begin->getCanonicalDecl())) {
            new_method.fun_type = 1;
          } else if (isa<CXXDestructorDecl>(
                         methods_begin->getCanonicalDecl())) {
            new_method.fun_type = 2;
          }
          temp_class.Functions.push_back(new_method);
          Function_list.push_back(new_method);
          current_Fun = new_method;

          methods_begin++;
        }

        //// 构造函数
        // auto class_ctors = classDecl->ctors();

        //// friends
        // auto class_friends = classDecl->friends();

        Class_list.push_back(temp_class);
        current_Class = temp_class;
      }
    }

    if (auto const *ifStmt = Result.Nodes.getNodeAs<IfStmt>("IfStmt")) {
      string loc = ifStmt->getBeginLoc().printToString(
          Result.Context->getSourceManager());
      if_loc.push_back(changes(loc));
    }

    if (auto const *varDecl = Result.Nodes.getNodeAs<VarDecl>("gvar")) {
      // 获取全局变量
      // cout << "获取全局变量" << endl;
      string var_name = varDecl->getNameAsString();
      string var_type = varDecl->getType().getAsString();
      string type_decl_loc = "";
      if (varDecl->getType()->getAsCXXRecordDecl() != NULL)
        type_decl_loc = varDecl->getType()
                            ->getAsCXXRecordDecl()
                            ->getBeginLoc()
                            .printToString(Result.Context->getSourceManager());
      string decl_loc = varDecl->getBeginLoc().printToString(
          Result.Context->getSourceManager());
      g_var new_g_var;
      new_g_var.name = var_name;
      new_g_var.type = var_type;
      new_g_var.type_decl_loc = changes(type_decl_loc);
      new_g_var.decl_loc = changes(decl_loc);
      global_var.push_back(new_g_var);
    }

    if (auto const *functionDecl =
            Result.Nodes.getNodeAs<FunctionDecl>("FunctiondFeclWithCall")) {
      // cout << "普通函数声明" << endl;
      string isbody = "1";
      if (!functionDecl
               ->hasBody()) // 判断函数是否有函数体，仅有一个声明的没有实现的函数停止解析
      {
        isbody = "0";
      }
      string loc = functionDecl->getSourceRange().getBegin().printToString(
          Result.Context->getSourceManager()); // 获得函数声明的位置
      loc = changes(loc);
      // cout << loc << endl;
      string File_path = split(loc, ":")[0] + ":" + split(loc, ":")[1];
      // 以下就是获取函数的名称、参数、返回值相关信息，接口描述都很清晰，主要注意函数参数获取方式用到的
      // QualType 使用方法
      functionname = functionDecl->getNameAsString();
      int find = 0;
      if (functionname != current_Fun.function_name) {
        for (int i = 0; i < Function_list.size(); i++) {
          if (functionname == Function_list[i].function_name &&
              loc == Function_list[i].function_location) {
            find = 1;
            current_Fun = Function_list[i];
            break;
          }
        }
        if (find == 0) {

          // 获得函数参数列表
          ParmVarDecl *const *param_temp;
          string param_type;
          string param_name;
          vector<param> params;
          auto f_parameters = functionDecl->parameters();
          int length = f_parameters.size();
          if (f_parameters.size() != 0) {
            param_temp = f_parameters.begin();
            for (int i = 0; i < f_parameters.size(); i++) {
              param_type = param_temp[i]->getType().getAsString();
              string type_decl_loc = "";
              if (param_temp[i]->getType()->getAsCXXRecordDecl() != NULL)
                type_decl_loc =
                    param_temp[i]
                        ->getType()
                        ->getAsCXXRecordDecl()
                        ->getBeginLoc()
                        .printToString(Result.Context->getSourceManager());

              param_name = param_temp[i]->getNameAsString();
              param pp;
              pp.name = param_name;
              pp.type = param_type;
              pp.type_decl_loc = changes(type_decl_loc);
              params.push_back(pp);
            }
          }

          Function_Constraint f_temp;
          f_temp.function_name = functionname;
          f_temp.function_location = loc;
          f_temp.isbody = isbody;

          f_temp.file_path = File_path;
          string start =
              functionDecl->getSourceRange().getBegin().printToString(
                  Result.Context->getSourceManager());
          start = changes(start);
          f_temp.start = split(start, ":")[2];
          string end = functionDecl->getSourceRange().getEnd().printToString(
              Result.Context->getSourceManager());
          end = changes(end);
          f_temp.end = split(end, ":")[2];

          QualType QT = functionDecl->getReturnType();
          string type_decl_loc = "";
          if (functionDecl->getType()->getAsCXXRecordDecl() != NULL)
            type_decl_loc =
                functionDecl->getReturnType()
                    ->getAsCXXRecordDecl()
                    ->getBeginLoc()
                    .printToString(Result.Context->getSourceManager());
          std::string TypeStr = QT.getAsString();
          f_temp.return_type = type_decl_loc + "$$" + TypeStr;
          f_temp.params = params;
          fun_count++;
          current_Fun = f_temp;
          Function_list.push_back(f_temp);
        }
      }
    }

    if (auto const *ConstructorDecl =
            Result.Nodes.getNodeAs<CXXConstructorDecl>("CXXConstructorDecl")) {
      // 类构造函数
      // cout << "类构造函数声明" << endl;
      string name = ConstructorDecl->getNameAsString();
      string loc = ConstructorDecl->getBeginLoc().printToString(
          Result.Context->getSourceManager());
      loc = changes(loc);
      for (int i = 0; i < Function_list.size(); i++) {
        if (name == Function_list[i].function_name &&
            loc == Function_list[i].function_location)
          current_Fun = Function_list[i];
      }
    }

    if (auto const *MethodDecl =
            Result.Nodes.getNodeAs<CXXMethodDecl>("CXXMethodDecl")) {
      // 类成员函数
      // cout << "类成员函数声明" << endl;
      string name = MethodDecl->getNameAsString();
      string loc = MethodDecl->getBeginLoc().printToString(
          Result.Context->getSourceManager());
      loc = changes(loc);
      for (int i = 0; i < Function_list.size(); i++) {
        if (name == Function_list[i].function_name &&
            loc == Function_list[i].function_location)
          current_Fun = Function_list[i];
      }
    }

    if (auto const *memberExpr =
            Result.Nodes.getNodeAs<MemberExpr>("MemberExpr")) {
      // 获取调用的是函数还是变量
      // cout << "获取类方法调用或类成员变量使用" << endl;
      string type = memberExpr->getType().getAsString();

      if (type == "<bound member function type>" ||
          (type.find("(") != string::npos && type.find(")") != string::npos)) {
        // 调用成员函数
        string method_name = memberExpr->getMemberDecl()->getNameAsString();
        string method_decl_loc =
            memberExpr->getMemberDecl()->getBeginLoc().printToString(
                Result.Context->getSourceManager());
        method_decl_loc = changes(method_decl_loc);
        string method_call_loc = memberExpr->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        method_call_loc = changes(method_call_loc);
        string method_return_type =
            memberExpr->getMemberDecl()->getType().getAsString();
        string method_class = memberExpr->getBase()->getType().getAsString();
        Call_Fun_Info new_call_func;
        new_call_func.name = method_name;
        new_call_func.Decl_Loc = method_decl_loc;
        new_call_func.CallExpr_Loc = method_call_loc;
        new_call_func.return_type = method_return_type;
        new_call_func.decl_class = method_class;
        /*Function_Constraint fun = current_Fun;
        int find = 0;
        for (int i = 0; i < fun.call_fun.size(); i++)
        {
            if (fun.call_fun[i].name == method_name && fun.call_fun[i].Decl_Loc
        == method_decl_loc && fun.call_fun[i].CallExpr_Loc == method_call_loc)
                find = 1;

        }

        if (find == 0)
        {
            for (int i = 0; i < Function_list.size(); i++)
            {
                if (current_Fun.function_name == Function_list[i].function_name
        && current_Fun.function_location == Function_list[i].function_location)
                {
                    Function_list[i].call_fun.push_back(new_call_func);
                }
            }
        }*/

      } else {
        // cout << "aaa" << endl;
        // 调用成员变量或成员函数
        string field_type =
            memberExpr->getMemberDecl()->getType().getAsString();
        string type_decl_loc = "";
        if (memberExpr->getType()->getAsCXXRecordDecl() != NULL)
          type_decl_loc =
              memberExpr->getMemberDecl()
                  ->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());
        string field_name = memberExpr->getMemberDecl()->getNameAsString();
        string field_decl_loc =
            memberExpr->getMemberDecl()->getBeginLoc().printToString(
                Result.Context->getSourceManager());
        field_decl_loc = changes(field_decl_loc);
        string field_using_loc = memberExpr->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        field_using_loc = changes(field_using_loc);

        string decl_class = memberExpr->getBase()->getType().getAsString();
        string class_decl_loc = "";
        if (memberExpr->getBase()->getType()->getAsCXXRecordDecl() != NULL)
          class_decl_loc =
              memberExpr->getBase()
                  ->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());

        var_using new_field_using;
        new_field_using.variable_name = field_name;
        new_field_using.type = field_type;
        new_field_using.type_decl_loc = changes(type_decl_loc);
        new_field_using.decl_loc = field_decl_loc;
        new_field_using.using_loc = field_using_loc;
        new_field_using.decl_class = decl_class;
        new_field_using.class_decl_loc = changes(class_decl_loc);

        int find = 0;
        class_Constraint cur_class = current_Class;
        for (int i = 0; i < cur_class.variables.size(); i++) {
          if (cur_class.variables[i].variable_name == field_name &&
              cur_class.variables[i].decl_loc == field_decl_loc &&
              cur_class.variables[i].using_loc == field_using_loc)
            find = 1;
        }
        if (find == 0) {
          for (int i = 0; i < Class_list.size(); i++) {
            if (current_Class.class_name == Class_list[i].class_name &&
                current_Class.decl_loc == Class_list[i].decl_loc) {
              Class_list[i].variables.push_back(new_field_using);
            }
          }
        }
      }
    }

    if (auto const *memberExpr =
            Result.Nodes.getNodeAs<MemberExpr>("fun_memberExpr")) {
      // 获取调用的是函数还是变量
      // cout << "获取类方法调用或类成员变量使用" << endl;
      string type = memberExpr->getType().getAsString();

      if (type == "<bound member function type>" ||
          (type.find("(") != string::npos && type.find(")") != string::npos)) {
        // 调用成员函数
        // cout << "aa" << endl;
        string method_name = memberExpr->getMemberDecl()->getNameAsString();
        string method_decl_loc =
            memberExpr->getMemberDecl()->getBeginLoc().printToString(
                Result.Context->getSourceManager());
        method_decl_loc = changes(method_decl_loc);
        string method_call_loc = memberExpr->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        method_call_loc = changes(method_call_loc);
        string method_return_type =
            memberExpr->getMemberDecl()->getType().getAsString();
        string method_class = memberExpr->getBase()->getType().getAsString();
        Call_Fun_Info new_call_func;
        new_call_func.name = method_name;
        new_call_func.Decl_Loc = method_decl_loc;
        new_call_func.CallExpr_Loc = method_call_loc;
        new_call_func.return_type = method_return_type;
        new_call_func.decl_class = method_class;
        /*Function_Constraint fun = current_Fun;
        int find = 0;
        for (int i = 0; i < fun.call_fun.size(); i++)
        {
            if (fun.call_fun[i].name == method_name && fun.call_fun[i].Decl_Loc
        == method_decl_loc && fun.call_fun[i].CallExpr_Loc == method_call_loc)
                find = 1;

        }

        if (find == 0)
        {
            for (int i = 0; i < Function_list.size(); i++)
            {
                if (current_Fun.function_name == Function_list[i].function_name
        && current_Fun.function_location == Function_list[i].function_location)
                {
                    Function_list[i].call_fun.push_back(new_call_func);
                }
            }
        }*/

      } else {
        // cout << "bb" << endl;
        // 调用成员变量或成员函数
        string field_type =
            memberExpr->getMemberDecl()->getType().getAsString();
        string type_decl_loc = "";
        if (memberExpr->getMemberDecl()->getType()->getAsCXXRecordDecl() !=
            NULL)
          type_decl_loc =
              memberExpr->getMemberDecl()
                  ->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());
        string field_name = memberExpr->getMemberDecl()->getNameAsString();
        string field_decl_loc =
            memberExpr->getMemberDecl()->getBeginLoc().printToString(
                Result.Context->getSourceManager());
        field_decl_loc = changes(field_decl_loc);
        string field_using_loc = memberExpr->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        field_using_loc = changes(field_using_loc);

        string decl_class = memberExpr->getBase()->getType().getAsString();
        string class_decl_loc = "";
        if (memberExpr->getBase()->getType()->getAsCXXRecordDecl() != NULL)
          class_decl_loc =
              memberExpr->getBase()
                  ->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());

        var_using new_field_using;
        new_field_using.variable_name = field_name;
        new_field_using.type = field_type;
        new_field_using.type_decl_loc = changes(type_decl_loc);
        new_field_using.decl_loc = field_decl_loc;
        new_field_using.using_loc = field_using_loc;
        new_field_using.decl_class = decl_class;
        new_field_using.class_decl_loc = changes(class_decl_loc);

        int find = 0;
        Function_Constraint fun = current_Fun;
        for (int i = 0; i < fun.variables.size(); i++) {
          if (fun.variables[i].variable_name == field_name &&
              fun.variables[i].decl_loc == field_decl_loc &&
              fun.variables[i].using_loc == field_using_loc)
            find = 1;
        }
        if (find == 0) {
          for (int i = 0; i < Function_list.size(); i++) {
            if (current_Fun.function_name == Function_list[i].function_name &&
                current_Fun.function_location ==
                    Function_list[i].function_location) {
              Function_list[i].variables.push_back(new_field_using);
            }
          }
        }
      }
    }

    if (auto const *memberExpr =
            Result.Nodes.getNodeAs<MemberExpr>("cfun_memberExpr")) {
      // 获取调用的是函数还是变量
      // cout << "获取类方法调用或类成员变量使用" << endl;
      string type = memberExpr->getType().getAsString();

      if (type == "<bound member function type>" ||
          (type.find("(") != string::npos && type.find(")") != string::npos)) {
        // 调用成员函数
        // cout << "aa" << endl;
        string method_name = memberExpr->getMemberDecl()->getNameAsString();
        string method_decl_loc =
            memberExpr->getMemberDecl()->getBeginLoc().printToString(
                Result.Context->getSourceManager());
        method_decl_loc = changes(method_decl_loc);
        string method_call_loc = memberExpr->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        method_call_loc = changes(method_call_loc);
        string method_return_type =
            memberExpr->getMemberDecl()->getType().getAsString();
        string method_class = memberExpr->getBase()->getType().getAsString();
        Call_Fun_Info new_call_func;
        new_call_func.name = method_name;
        new_call_func.Decl_Loc = method_decl_loc;
        new_call_func.CallExpr_Loc = method_call_loc;
        new_call_func.return_type = method_return_type;
        new_call_func.decl_class = method_class;
        /*Function_Constraint fun = current_Fun;
        int find = 0;
        for (int i = 0; i < fun.call_fun.size(); i++)
        {
            if (fun.call_fun[i].name == method_name && fun.call_fun[i].Decl_Loc
        == method_decl_loc && fun.call_fun[i].CallExpr_Loc == method_call_loc)
                find = 1;

        }

        if (find == 0)
        {
            for (int i = 0; i < Function_list.size(); i++)
            {
                if (current_Fun.function_name == Function_list[i].function_name
        && current_Fun.function_location == Function_list[i].function_location)
                {
                    Function_list[i].call_fun.push_back(new_call_func);
                }
            }
        }*/

      } else {
        // cout << "bb" << endl;
        // 调用成员变量或成员函数
        if (current_Fun.function_name == "syncCall")
          cout << "1";
        string field_type =
            memberExpr->getMemberDecl()->getType().getAsString();
        string type_decl_loc = "";
        if (memberExpr->getMemberDecl()->getType()->getAsCXXRecordDecl() !=
            NULL)
          type_decl_loc =
              memberExpr->getMemberDecl()
                  ->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());
        string field_name = memberExpr->getMemberDecl()->getNameAsString();
        string field_decl_loc =
            memberExpr->getMemberDecl()->getBeginLoc().printToString(
                Result.Context->getSourceManager());
        field_decl_loc = changes(field_decl_loc);
        string field_using_loc = memberExpr->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        field_using_loc = changes(field_using_loc);

        string decl_class = memberExpr->getBase()->getType().getAsString();
        string class_decl_loc = "";
        if (memberExpr->getBase()->getType()->getAsCXXRecordDecl() != NULL)
          class_decl_loc =
              memberExpr->getBase()
                  ->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());

        var_using new_field_using;
        new_field_using.variable_name = field_name;
        new_field_using.type = field_type;
        new_field_using.type_decl_loc = changes(type_decl_loc);
        new_field_using.decl_loc = field_decl_loc;
        new_field_using.using_loc = field_using_loc;
        new_field_using.decl_class = decl_class;
        new_field_using.class_decl_loc = changes(class_decl_loc);

        int find = 0;
        Function_Constraint fun = current_Fun;
        for (int i = 0; i < fun.variables.size(); i++) {
          if (fun.variables[i].variable_name == field_name &&
              fun.variables[i].decl_loc == field_decl_loc &&
              fun.variables[i].using_loc == field_using_loc)
            find = 1;
        }
        if (find == 0) {
          for (int i = 0; i < Function_list.size(); i++) {
            if (current_Fun.function_name == Function_list[i].function_name &&
                current_Fun.function_location ==
                    Function_list[i].function_location) {
              Function_list[i].variables.push_back(new_field_using);
            }
          }
        }
      }
    }

    if (auto const *memberExpr =
            Result.Nodes.getNodeAs<MemberExpr>("class_memberExpr")) {
      // 获取调用的是函数还是变量
      // cout << "获取类方法调用或类成员变量使用" << endl;
      string type = memberExpr->getType().getAsString();

      if (type == "<bound member function type>" ||
          (type.find("(") != string::npos && type.find(")") != string::npos)) {
        // 调用成员函数
        // cout << "aa" << endl;
        string method_name = memberExpr->getMemberDecl()->getNameAsString();
        string method_decl_loc =
            memberExpr->getMemberDecl()->getBeginLoc().printToString(
                Result.Context->getSourceManager());
        method_decl_loc = changes(method_decl_loc);
        string method_call_loc = memberExpr->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        method_call_loc = changes(method_call_loc);
        string method_return_type =
            memberExpr->getMemberDecl()->getType().getAsString();
        string method_class = memberExpr->getBase()->getType().getAsString();
        Call_Fun_Info new_call_func;
        new_call_func.name = method_name;
        new_call_func.Decl_Loc = method_decl_loc;
        new_call_func.CallExpr_Loc = method_call_loc;
        new_call_func.return_type = method_return_type;
        new_call_func.decl_class = method_class;
        /*Function_Constraint fun = current_Fun;
        int find = 0;
        for (int i = 0; i < fun.call_fun.size(); i++)
        {
            if (fun.call_fun[i].name == method_name && fun.call_fun[i].Decl_Loc
        == method_decl_loc && fun.call_fun[i].CallExpr_Loc == method_call_loc)
                find = 1;

        }

        if (find == 0)
        {
            for (int i = 0; i < Function_list.size(); i++)
            {
                if (current_Fun.function_name == Function_list[i].function_name
        && current_Fun.function_location == Function_list[i].function_location)
                {
                    Function_list[i].call_fun.push_back(new_call_func);
                }
            }
        }*/

      } else {
        // cout << "bb" << endl;
        // 调用成员变量或成员函数
        string field_type =
            memberExpr->getMemberDecl()->getType().getAsString();
        string type_decl_loc = "";
        if (memberExpr->getMemberDecl()->getType()->getAsCXXRecordDecl() !=
            NULL)
          type_decl_loc =
              memberExpr->getMemberDecl()
                  ->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());
        string field_name = memberExpr->getMemberDecl()->getNameAsString();
        string field_decl_loc =
            memberExpr->getMemberDecl()->getBeginLoc().printToString(
                Result.Context->getSourceManager());
        field_decl_loc = changes(field_decl_loc);
        string field_using_loc = memberExpr->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        field_using_loc = changes(field_using_loc);

        string decl_class = memberExpr->getBase()->getType().getAsString();
        string class_decl_loc = "";
        if (memberExpr->getBase()->getType()->getAsCXXRecordDecl() != NULL)
          class_decl_loc =
              memberExpr->getBase()
                  ->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());

        var_using new_field_using;
        new_field_using.variable_name = field_name;
        new_field_using.type = field_type;
        new_field_using.type_decl_loc = changes(type_decl_loc);
        new_field_using.decl_loc = field_decl_loc;
        new_field_using.using_loc = field_using_loc;
        new_field_using.decl_class = decl_class;
        new_field_using.class_decl_loc = changes(class_decl_loc);

        int find = 0;
        class_Constraint cur_class = current_Class;
        for (int i = 0; i < cur_class.variables.size(); i++) {
          if (cur_class.variables[i].variable_name == field_name &&
              cur_class.variables[i].decl_loc == field_decl_loc &&
              cur_class.variables[i].using_loc == field_using_loc)
            find = 1;
        }
        if (find == 0) {
          for (int i = 0; i < Class_list.size(); i++) {
            if (current_Class.class_name == Class_list[i].class_name &&
                current_Class.decl_loc == Class_list[i].decl_loc) {
              if (field_type.find("ostream") == string::npos) {
                Class_list[i].variables.push_back(new_field_using);
              }
              /*else
              {
                  Call_Fun_Info new_call_fun;
                  new_call_fun.name = var_name;
                  new_call_fun.CallExpr_Loc = var_using_loc;
                  new_call_fun.Decl_Loc = var_decl_loc;
                  new_call_fun.return_type = var_type;
                  Function_list[i].call_fun.push_back(new_call_fun);
              }*/
            }
          }
        }
      }
    }

    if (auto const *callExpr = Result.Nodes.getNodeAs<CallExpr>("call_expr")) {
      // 获取函数名称
      auto if_func = callExpr->getDirectCallee();
      if (if_func == NULL) {
        // 不是函数调用，则为调用函数指针
        string call_loc = callExpr->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        call_loc = changes(call_loc);
        // 获取函数指针名称
        auto type = callExpr->getCallee()->getType().getAsString();
        auto callee = callExpr->getCallee();
        string pointer_fun_name;
        string pointer_fun_type;
        string pointer_fun_type_decl_loc;
        string pointer_fun_decl_loc;
        string struct_name;
        if (isa<ImplicitCastExpr>(callee)) {
          const ImplicitCastExpr *implicitCastExpr =
              cast<ImplicitCastExpr>(callee);
          if (isa<MemberExpr>(implicitCastExpr->getSubExpr())) {
            pointer_fun_name = cast<MemberExpr>(implicitCastExpr->getSubExpr())
                                   ->getMemberDecl()
                                   ->getNameAsString();
            pointer_fun_type = cast<MemberExpr>(implicitCastExpr->getSubExpr())
                                   ->getMemberDecl()
                                   ->getType()
                                   .getAsString();
            pointer_fun_decl_loc =
                cast<MemberExpr>(implicitCastExpr->getSubExpr())
                    ->getMemberDecl()
                    ->getBeginLoc()
                    .printToString(Result.Context->getSourceManager());
            pointer_fun_decl_loc = changes(pointer_fun_decl_loc);
          }
        }
        if (isa<ParenExpr>(callee)) {
          auto temp = cast<ParenExpr>(callee);
          pointer_fun_name = temp->getSubExpr()->getType().getAsString();
          pointer_fun_type = "void";
          pointer_fun_decl_loc = temp->getBeginLoc().printToString(
              Result.Context->getSourceManager());
          pointer_fun_decl_loc = changes(pointer_fun_decl_loc);
        }
        pointer_func new_pf;
        new_pf.name = pointer_fun_name;
        new_pf.type = pointer_fun_type;
        new_pf.loc = pointer_fun_decl_loc;
        new_pf.call_loc = call_loc;
        int find = 0;
        Function_Constraint fun = current_Fun;
        for (int i = 0; i < fun.call_pointer_func.size(); i++) {
          if (fun.call_pointer_func[i].name == new_pf.name &&
              fun.call_pointer_func[i].type == new_pf.type &&
              fun.call_pointer_func[i].loc == new_pf.loc)
            find = 1;
        }
        if (find == 0) {
          for (int i = 0; i < Function_list.size(); i++) {
            if (current_Fun.function_name == Function_list[i].function_name &&
                current_Fun.function_location ==
                    Function_list[i].function_location) {
              Function_list[i].call_pointer_func.push_back(new_pf);
            }
          }
        }
      } else {
        auto func = if_func;
        if (isa<FunctionDecl>(func)) {
          const FunctionDecl *Fun_Call = cast<FunctionDecl>(func);
          string Fun_Call_Name = Fun_Call->getNameAsString();
          // auto Call_Code = callexprtdec->
          string CallExpr_Loc =
              callExpr->getSourceRange().getBegin().printToString(
                  Result.Context->getSourceManager());
          CallExpr_Loc = changes(CallExpr_Loc);
          const FunctionDecl *Fun_Decl = cast<FunctionDecl>(if_func);
          string Decl_loc = Fun_Decl->getSourceRange().getBegin().printToString(
              Result.Context->getSourceManager());
          Decl_loc = changes(Decl_loc);
          string return_type = Fun_Call->getReturnType().getAsString();
          int find = 0;
          Function_Constraint fun = current_Fun;
          for (int i = 0; i < fun.call_fun.size(); i++) {
            if (fun.call_fun[i].name == Fun_Call_Name &&
                fun.call_fun[i].Decl_Loc == Decl_loc &&
                fun.call_fun[i].CallExpr_Loc == CallExpr_Loc)
              find = 1;
          }
          if (find == 0) {
            Call_Fun_Info call_fun;
            call_fun.name = Fun_Call_Name;
            call_fun.Decl_Loc = Decl_loc;
            call_fun.CallExpr_Loc = CallExpr_Loc;
            call_fun.return_type = return_type;
            for (int i = 0; i < Function_list.size(); i++) {
              if (current_Fun.function_name == Function_list[i].function_name &&
                  current_Fun.function_location ==
                      Function_list[i].function_location) {
                Function_list[i].call_fun.push_back(call_fun);
              }
            }
          }
        }
      }
    }

    if (auto const *binaryOperator =
            Result.Nodes.getNodeAs<BinaryOperator>("BinaryOperator")) {
      // 通过二元操作符寻找函数指针赋值
      string Opp = binaryOperator->getOpcodeStr().data();
      // 获取右部
      Expr *binaryOperator_right = binaryOperator->getRHS();
      if (isa<ImplicitCastExpr>(binaryOperator_right)) {
        const ImplicitCastExpr *implicitCastExpr =
            cast<ImplicitCastExpr>(binaryOperator_right);
        if (isa<DeclRefExpr>(implicitCastExpr->getSubExpr())) {
          auto declRef = cast<DeclRefExpr>(implicitCastExpr->getSubExpr());
          auto func = declRef->getDecl();
          if (isa<FunctionDecl>(func)) {
            const FunctionDecl *Fun_Call = cast<FunctionDecl>(func);
            string func_name = Fun_Call->getNameAsString();
            string func_decl_loc = Fun_Call->getBeginLoc().printToString(
                Result.Context->getSourceManager());
            func_decl_loc = changes(func_decl_loc);
            pointer_matched_func matched_fun;
            matched_fun.name = func_name;
            matched_fun.loc = func_decl_loc;
            // 获取左部
            Expr *binaryOperator_left = binaryOperator->getLHS();
            if (isa<MemberExpr>(binaryOperator_left) && Opp == "=") {
              auto memberExpr = cast<MemberExpr>(binaryOperator_left);
              string pointer_fun_name =
                  memberExpr->getMemberDecl()->getNameAsString();
              string pointer_fun_type =
                  memberExpr->getMemberDecl()->getType().getAsString();
              string pointer_fun_decl_loc =
                  memberExpr->getMemberDecl()->getBeginLoc().printToString(
                      Result.Context->getSourceManager());
              pointer_fun_decl_loc = changes(pointer_fun_decl_loc);
              pointer_func temp;
              for (int i = 0; i < pointer_func_list.size(); i++) {
                if (pointer_func_list[i].name == pointer_fun_name &&
                    pointer_func_list[i].loc == pointer_fun_decl_loc) {
                  temp = pointer_func_list[i];
                  pointer_func_list[i].matched_func_list.push_back(matched_fun);
                  break;
                }
              }

              if (temp.name == "" && temp.loc == "") {
                temp.name = pointer_fun_name;
                temp.type = pointer_fun_type;
                temp.loc = pointer_fun_decl_loc;
                temp.matched_func_list.push_back(matched_fun);
                pointer_func_list.push_back(temp);
              }
            }
          }
        }
      }
    }

    if (auto const *declRef =
            Result.Nodes.getNodeAs<DeclRefExpr>("fun_decl_ref")) {
      // 获取声明
      // cout << "获取函数调用或变量使用" << endl;
      auto func = declRef->getDecl();
      // string CallExpr_Loc =
      // declRef->getSourceRange().getBegin().printToString(Result.Context->getSourceManager());
      string type = func->getType().getAsString();
      if (isa<FunctionDecl>(func)) {
        // 调用函数
        const FunctionDecl *Fun_Call = cast<FunctionDecl>(func);
        string Fun_Call_Name = Fun_Call->getNameAsString();
        // auto Call_Code = callexprtdec->
        string CallExpr_Loc =
            declRef->getSourceRange().getBegin().printToString(
                Result.Context->getSourceManager());
        CallExpr_Loc = changes(CallExpr_Loc);
        const FunctionDecl *Fun_Decl = cast<FunctionDecl>(declRef->getDecl());
        string Decl_loc = Fun_Decl->getSourceRange().getBegin().printToString(
            Result.Context->getSourceManager());
        Decl_loc = changes(Decl_loc);

        string return_type = Fun_Call->getReturnType().getAsString();
        /*int find = 0;
        Function_Constraint fun = current_Fun;
        for (int i = 0; i < fun.call_fun.size(); i++)
        {
            if (fun.call_fun[i].name == Fun_Call_Name &&
        fun.call_fun[i].Decl_Loc == Decl_loc && fun.call_fun[i].CallExpr_Loc ==
        CallExpr_Loc) find = 1;

        }
        if (find == 0)
        {
            Call_Fun_Info call_fun;
            call_fun.name = Fun_Call_Name;
            call_fun.Decl_Loc = Decl_loc;
            call_fun.CallExpr_Loc = CallExpr_Loc;
            call_fun.return_type = return_type;
            for (int i = 0; i < Function_list.size(); i++)
            {
                if (current_Fun.function_name == Function_list[i].function_name
        && current_Fun.function_location == Function_list[i].function_location)
                {
                    Function_list[i].call_fun.push_back(call_fun);
                }
            }
        }*/
      } else {
        // 类成员方法使用变量(局部变量和全局变量)
        string var_type = func->getType().getAsString();
        string type_decl_loc = "";
        if (func->getType()->getAsCXXRecordDecl() != NULL)
          type_decl_loc =
              func->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());
        string var_name = func->getNameAsString();
        string var_decl_loc = func->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        var_decl_loc = changes(var_decl_loc);
        string var_using_loc = declRef->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        var_using_loc = changes(var_using_loc);

        int find = 0;
        Function_Constraint fun = current_Fun;
        for (int i = 0; i < fun.variables.size(); i++) {
          if (fun.variables[i].variable_name == var_name &&
              fun.variables[i].decl_loc == var_decl_loc &&
              fun.variables[i].using_loc == var_using_loc)
            find = 1;
        }
        if (find == 0) {
          for (int i = 0; i < Function_list.size(); i++) {
            if (current_Fun.function_name == Function_list[i].function_name &&
                current_Fun.function_location ==
                    Function_list[i].function_location) {
              if (var_type.find("ostream") == string::npos) {
                var_using new_used_var;
                new_used_var.variable_name = var_name;
                new_used_var.type = var_type;
                new_used_var.type_decl_loc = changes(type_decl_loc);
                new_used_var.decl_loc = var_decl_loc;
                new_used_var.using_loc = var_using_loc;
                Function_list[i].variables.push_back(new_used_var);
              } else {
                Call_Fun_Info new_call_fun;
                new_call_fun.name = var_name;
                new_call_fun.CallExpr_Loc = var_using_loc;
                new_call_fun.Decl_Loc = var_decl_loc;
                new_call_fun.return_type = var_type;
                Function_list[i].call_fun.push_back(new_call_fun);
              }
            }
          }
        }
      }
    }

    if (auto const *declRef =
            Result.Nodes.getNodeAs<DeclRefExpr>("cfun_decl_ref")) {
      // 获取声明
      // cout << "获取函数调用或变量使用" << endl;
      auto func = declRef->getDecl();
      // string CallExpr_Loc =
      // declRef->getSourceRange().getBegin().printToString(Result.Context->getSourceManager());
      string type = func->getType().getAsString();
      if (isa<FunctionDecl>(func)) {
        // 调用函数
        const FunctionDecl *Fun_Call = cast<FunctionDecl>(func);
        string Fun_Call_Name = Fun_Call->getNameAsString();
        // auto Call_Code = callexprtdec->
        string CallExpr_Loc =
            declRef->getSourceRange().getBegin().printToString(
                Result.Context->getSourceManager());
        CallExpr_Loc = changes(CallExpr_Loc);
        const FunctionDecl *Fun_Decl = cast<FunctionDecl>(declRef->getDecl());
        string Decl_loc = Fun_Decl->getSourceRange().getBegin().printToString(
            Result.Context->getSourceManager());
        Decl_loc = changes(Decl_loc);

        string return_type = Fun_Call->getReturnType().getAsString();
        /*int find = 0;
        Function_Constraint fun = current_Fun;
        for (int i = 0; i < fun.call_fun.size(); i++)
        {
            if (fun.call_fun[i].name == Fun_Call_Name &&
        fun.call_fun[i].Decl_Loc == Decl_loc && fun.call_fun[i].CallExpr_Loc ==
        CallExpr_Loc) find = 1;

        }
        if (find == 0)
        {
            Call_Fun_Info call_fun;
            call_fun.name = Fun_Call_Name;
            call_fun.Decl_Loc = Decl_loc;
            call_fun.CallExpr_Loc = CallExpr_Loc;
            call_fun.return_type = return_type;
            for (int i = 0; i < Function_list.size(); i++)
            {
                if (current_Fun.function_name == Function_list[i].function_name
        && current_Fun.function_location == Function_list[i].function_location)
                {
                    Function_list[i].call_fun.push_back(call_fun);
                }
            }
        }*/
      } else {
        // 类成员方法使用变量(局部变量和全局变量)
        string var_type = func->getType().getAsString();
        string type_decl_loc = "";
        if (func->getType()->getAsCXXRecordDecl() != NULL)
          type_decl_loc =
              func->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());
        string var_name = func->getNameAsString();
        string var_decl_loc = func->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        var_decl_loc = changes(var_decl_loc);
        string var_using_loc = declRef->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        var_using_loc = changes(var_using_loc);

        int find = 0;
        Function_Constraint fun = current_Fun;
        for (int i = 0; i < fun.variables.size(); i++) {
          if (fun.variables[i].variable_name == var_name &&
              fun.variables[i].decl_loc == var_decl_loc &&
              fun.variables[i].using_loc == var_using_loc)
            find = 1;
        }
        if (find == 0) {
          for (int i = 0; i < Function_list.size(); i++) {
            if (current_Fun.function_name == Function_list[i].function_name &&
                current_Fun.function_location ==
                    Function_list[i].function_location) {
              if (var_type.find("ostream") == string::npos &&
                  var_type.find("istream") == string::npos) {
                var_using new_used_var;
                new_used_var.variable_name = var_name;
                new_used_var.type = var_type;
                new_used_var.type_decl_loc = changes(type_decl_loc);
                new_used_var.decl_loc = var_decl_loc;
                new_used_var.using_loc = var_using_loc;
                Function_list[i].variables.push_back(new_used_var);
              } else {
                Call_Fun_Info new_call_fun;
                new_call_fun.name = var_name;
                new_call_fun.CallExpr_Loc = var_using_loc;
                new_call_fun.Decl_Loc = var_decl_loc;
                new_call_fun.return_type = var_type;
                Function_list[i].call_fun.push_back(new_call_fun);
              }
            }
          }
        }
      }
    }

    if (auto const *declRef =
            Result.Nodes.getNodeAs<DeclRefExpr>("class_decl_ref")) {
      // 获取声明
      // cout << "获取函数调用或变量使用" << endl;
      auto func = declRef->getDecl();
      // string CallExpr_Loc =
      // declRef->getSourceRange().getBegin().printToString(Result.Context->getSourceManager());
      string type = func->getType().getAsString();
      if (isa<FunctionDecl>(func) || type == "std::ostream") {
        //// 调用函数
        // const FunctionDecl* Fun_Call = cast<FunctionDecl>(func);
        // string Fun_Call_Name = Fun_Call->getNameAsString();
        ////auto Call_Code = callexprtdec->
        // string CallExpr_Loc =
        // declRef->getSourceRange().getBegin().printToString(Result.Context->getSourceManager());
        // CallExpr_Loc = changes(CallExpr_Loc);
        // const FunctionDecl* Fun_Decl =
        // cast<FunctionDecl>(declRef->getDecl()); string Decl_loc =
        // Fun_Decl->getSourceRange().getBegin().printToString(Result.Context->getSourceManager());
        // Decl_loc = changes(Decl_loc);

        /*string return_type = Fun_Call->getReturnType().getAsString();
        int find = 0;
        Function_Constraint fun = current_Fun;
        for (int i = 0; i < fun.call_fun.size(); i++)
        {
            if (fun.call_fun[i].name == Fun_Call_Name &&
        fun.call_fun[i].Decl_Loc == Decl_loc && fun.call_fun[i].CallExpr_Loc ==
        CallExpr_Loc) find = 1;

        }
        if (find == 0)
        {
            Call_Fun_Info call_fun;
            call_fun.name = Fun_Call_Name;
            call_fun.Decl_Loc = Decl_loc;
            call_fun.CallExpr_Loc = CallExpr_Loc;
            call_fun.return_type = return_type;
            for (int i = 0; i < Function_list.size(); i++)
            {
                if (current_Fun.function_name == Function_list[i].function_name
        && current_Fun.function_location == Function_list[i].function_location)
                {
                    Function_list[i].call_fun.push_back(call_fun);
                }
            }
        }*/
      } else {
        // 类使用变量(局部变量和全局变量)
        string var_type = func->getType().getAsString();
        string type_decl_loc = "";
        if (func->getType()->getAsCXXRecordDecl() != NULL)
          type_decl_loc =
              func->getType()
                  ->getAsCXXRecordDecl()
                  ->getBeginLoc()
                  .printToString(Result.Context->getSourceManager());
        string var_name = func->getNameAsString();
        string var_decl_loc = func->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        var_decl_loc = changes(var_decl_loc);
        string var_using_loc = declRef->getBeginLoc().printToString(
            Result.Context->getSourceManager());
        var_using_loc = changes(var_using_loc);

        if (var_name != "") {
          int find = 0;
          class_Constraint cur_class = current_Class;
          for (int i = 0; i < cur_class.variables.size(); i++) {
            if (cur_class.variables[i].variable_name == var_name &&
                cur_class.variables[i].decl_loc == var_decl_loc &&
                cur_class.variables[i].using_loc == var_using_loc)
              find = 1;
          }
          if (find == 0) {
            for (int i = 0; i < Class_list.size(); i++) {
              if (current_Class.class_name == Class_list[i].class_name &&
                  current_Class.decl_loc == Class_list[i].decl_loc) {
                if (var_type.find("ostream") == string::npos) {
                  var_using new_used_var;
                  new_used_var.variable_name = var_name;
                  new_used_var.type = var_type;
                  new_used_var.type_decl_loc = changes(type_decl_loc);
                  new_used_var.decl_loc = var_decl_loc;
                  new_used_var.using_loc = var_using_loc;
                  Class_list[i].variables.push_back(new_used_var);
                }
                /*else
                {
                    Call_Fun_Info new_call_fun;
                    new_call_fun.name = var_name;
                    new_call_fun.CallExpr_Loc = var_using_loc;
                    new_call_fun.Decl_Loc = var_decl_loc;
                    new_call_fun.return_type = var_type;
                    Function_list[i].call_fun.push_back(new_call_fun);
                }*/
              }
            }
          }
        }
      }
    }

    // if (auto const* parenExpr =
    // Result.Nodes.getNodeAs<ParenExpr>("cfun_parenExpr"))
    //{
    //     cout << "cfun_parenExpr" << endl;
    //     auto paren = parenExpr;
    //     string begin_loc =
    //     paren->getBeginLoc().printToString(Result.Context->getSourceManager());
    //     begin_loc = changes(begin_loc);
    //     string end_loc =
    //     paren->getEndLoc().printToString(Result.Context->getSourceManager());
    //     end_loc = changes(end_loc);

    //    string var_name = begin_loc;
    //    string var_decl_loc = begin_loc;
    //    string var_using_loc = begin_loc;
    //    string var_type = paren->getType().getAsString();

    //    int find = 0;
    //    Function_Constraint fun = current_Fun;
    //    for (int i = 0; i < fun.variables.size(); i++)
    //    {
    //        if (fun.variables[i].variable_name == var_name &&
    //        fun.variables[i].decl_loc == var_decl_loc &&
    //        fun.variables[i].using_loc == var_using_loc)
    //            find = 1;

    //    }
    //    if (find == 0)
    //    {
    //        for (int i = 0; i < Function_list.size(); i++)
    //        {
    //            if (current_Fun.function_name ==
    //            Function_list[i].function_name &&
    //            current_Fun.function_location ==
    //            Function_list[i].function_location)
    //            {
    //                if (var_type.find("ostream") == string::npos)
    //                {
    //                    var_using new_used_var;
    //                    new_used_var.variable_name = var_name;
    //                    new_used_var.type = var_type;
    //                    new_used_var.type_decl_loc = changes(var_decl_loc);
    //                    new_used_var.decl_loc = var_decl_loc;
    //                    new_used_var.using_loc = var_using_loc;
    //                    Function_list[i].variables.push_back(new_used_var);
    //                }
    //                else
    //                {
    //                    Call_Fun_Info new_call_fun;
    //                    new_call_fun.name = var_name;
    //                    new_call_fun.CallExpr_Loc = var_using_loc;
    //                    new_call_fun.Decl_Loc = var_decl_loc;
    //                    new_call_fun.return_type = var_type;
    //                    Function_list[i].call_fun.push_back(new_call_fun);
    //                }
    //            }
    //        }
    //    }
    //}

    // if (auto const* parenExpr =
    // Result.Nodes.getNodeAs<ParenExpr>("fun_parenExpr"))
    //{
    //     auto paren = parenExpr;
    //     string begin_loc =
    //     paren->getBeginLoc().printToString(Result.Context->getSourceManager());
    //     begin_loc = changes(begin_loc);
    //     string end_loc =
    //     paren->getEndLoc().printToString(Result.Context->getSourceManager());
    //     end_loc = changes(end_loc);

    //    string var_name = begin_loc;
    //    string var_decl_loc = begin_loc;
    //    string var_using_loc = begin_loc;
    //    string var_type = paren->getType().getAsString();

    //    int find = 0;
    //    Function_Constraint fun = current_Fun;
    //    for (int i = 0; i < fun.variables.size(); i++)
    //    {
    //        if (fun.variables[i].variable_name == var_name &&
    //        fun.variables[i].decl_loc == var_decl_loc &&
    //        fun.variables[i].using_loc == var_using_loc)
    //            find = 1;

    //    }
    //    if (find == 0)
    //    {
    //        for (int i = 0; i < Function_list.size(); i++)
    //        {
    //            if (current_Fun.function_name ==
    //            Function_list[i].function_name &&
    //            current_Fun.function_location ==
    //            Function_list[i].function_location)
    //            {
    //                if (var_type.find("ostream") == string::npos)
    //                {
    //                    var_using new_used_var;
    //                    new_used_var.variable_name = var_name;
    //                    new_used_var.type = var_type;
    //                    new_used_var.type_decl_loc = changes(var_decl_loc);
    //                    new_used_var.decl_loc = var_decl_loc;
    //                    new_used_var.using_loc = var_using_loc;
    //                    Function_list[i].variables.push_back(new_used_var);
    //                }
    //                else
    //                {
    //                    Call_Fun_Info new_call_fun;
    //                    new_call_fun.name = var_name;
    //                    new_call_fun.CallExpr_Loc = var_using_loc;
    //                    new_call_fun.Decl_Loc = var_decl_loc;
    //                    new_call_fun.return_type = var_type;
    //                    Function_list[i].call_fun.push_back(new_call_fun);
    //                }
    //            }
    //        }
    //    }
    //}

    // if (auto const* parenExpr =
    // Result.Nodes.getNodeAs<ParenExpr>("class_parenExpr"))
    //{
    //     auto paren = parenExpr;
    //     string begin_loc =
    //     paren->getBeginLoc().printToString(Result.Context->getSourceManager());
    //     begin_loc = changes(begin_loc);
    //     string end_loc =
    //     paren->getEndLoc().printToString(Result.Context->getSourceManager());
    //     end_loc = changes(end_loc);

    //    string var_name = begin_loc;
    //    string var_decl_loc = begin_loc;
    //    string var_using_loc = begin_loc;
    //    string var_type = paren->getType().getAsString();

    //    if (var_name != "")
    //    {
    //        int find = 0;
    //        class_Constraint cur_class = current_Class;
    //        for (int i = 0; i < cur_class.variables.size(); i++)
    //        {
    //            if (cur_class.variables[i].variable_name == var_name &&
    //            cur_class.variables[i].decl_loc == var_decl_loc &&
    //            cur_class.variables[i].using_loc == var_using_loc)
    //                find = 1;

    //        }
    //        if (find == 0)
    //        {
    //            for (int i = 0; i < Class_list.size(); i++)
    //            {
    //                if (current_Class.class_name == Class_list[i].class_name
    //                && current_Class.decl_loc == Class_list[i].decl_loc)
    //                {
    //                    if (var_type.find("ostream") == string::npos)
    //                    {
    //                        var_using new_used_var;
    //                        new_used_var.variable_name = var_name;
    //                        new_used_var.type = var_type;
    //                        new_used_var.type_decl_loc = changes(begin_loc);
    //                        new_used_var.decl_loc = var_decl_loc;
    //                        new_used_var.using_loc = var_using_loc;
    //                        Class_list[i].variables.push_back(new_used_var);
    //                    }
    //                    /*else
    //                    {
    //                        Call_Fun_Info new_call_fun;
    //                        new_call_fun.name = var_name;
    //                        new_call_fun.CallExpr_Loc = var_using_loc;
    //                        new_call_fun.Decl_Loc = var_decl_loc;
    //                        new_call_fun.return_type = var_type;
    //                        Function_list[i].call_fun.push_back(new_call_fun);
    //                    }*/
    //                }
    //            }
    //        }
    //    }
    //}
    //

    // 如果解析成功的话
    if_success = "0";

    return;
  }
};

class MyFrontendAction : public ASTFrontendAction {
public:
  MyFrontendAction() = default;
  void EndSourceFileAction() override {
    auto m = getCompilerInstance().getDiagnostics().getNumWarnings();
    // spdlog::info("{} Warning\n", m);
  }
  unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &CI,
                                            StringRef file) override {
    llvm::errs() << "** Creating AST consumer for: " << file << "\n";
    auto m = CI.getDiagnostics().getNumWarnings();
    // spdlog::info("{}", m);
    /*auto decl_matcher = decl(isExpansionInMainFile(),
    hasDeclContext(translationUnitDecl())
    ).bind("Decl_node");*/

    auto decl_matcher = translationUnitDecl().bind("TranslationUnitDecl");

    auto FuncDeclMatcher =
        functionDecl(
            isExpansionInMainFile(),
            // anyOf(forEachDescendant(callExpr().bind("callExprFunction")),
            // unless(forEachDescendant(callExpr().bind("callExprFunction")))),
            anyOf(
                forEachDescendant(
                    declRefExpr(isExpansionInMainFile()).bind("cfun_decl_ref")),
                unless(forEachDescendant(declRefExpr(isExpansionInMainFile())
                                             .bind("cfun_decl_ref")))),
            anyOf(forEachDescendant(memberExpr(isExpansionInMainFile())
                                        .bind("cfun_memberExpr")),
                  unless(forEachDescendant(memberExpr(isExpansionInMainFile())
                                               .bind("cfun_memberExpr"))))
            // anyOf(forEachDescendant(parenExpr(isExpansionInMainFile()).bind("cfun_parenExpr")),
            // unless(forEachDescendant(parenExpr(isExpansionInMainFile()).bind("cfun_parenExpr"))))
            )
            .bind("FunctiondFeclWithCall");

    auto refExpr = declRefExpr(isExpansionInMainFile()).bind("declRefExpr");

    auto classMatcher =
        cxxRecordDecl(
            isExpansionInMainFile(),
            anyOf(forEachDescendant(declRefExpr(isExpansionInMainFile())
                                        .bind("class_decl_ref")),
                  unless(forEachDescendant(declRefExpr(isExpansionInMainFile())
                                               .bind("class_decl_ref")))),
            anyOf(forEachDescendant(memberExpr(isExpansionInMainFile())
                                        .bind("class_memberExpr")),
                  unless(forEachDescendant(memberExpr(isExpansionInMainFile())
                                               .bind("class_memberExpr"))))
            // anyOf(forEachDescendant(parenExpr(isExpansionInMainFile()).bind("cfun_parenExpr")),
            // unless(forEachDescendant(parenExpr(isExpansionInMainFile()).bind("class_parenExpr"))))
            )
            .bind("CXXRecordDecl");

    auto MemberCallExpr =
        cxxMemberCallExpr(isExpansionInMainFile()).bind("CXXMemberCallExpr");

    auto ConstructorDecl =
        cxxConstructorDecl(isExpansionInMainFile()).bind("CXXConstructorDecl");

    auto mmemberExpr = memberExpr(isExpansionInMainFile())
                           .bind("MemberExpr"); // 使用成员变量或者成员方法

    DeclarationMatcher GlobalVarMatcher =
        varDecl(isExpansionInMainFile(), hasGlobalStorage(),
                unless(hasAncestor(functionDecl()))

                    )
            .bind("gvar");

    auto MethodDecl =
        cxxMethodDecl(
            isExpansionInMainFile(),
            anyOf(
                forEachDescendant(
                    declRefExpr(isExpansionInMainFile()).bind("fun_decl_ref")),
                unless(forEachDescendant(declRefExpr(isExpansionInMainFile())
                                             .bind("fun_decl_ref")))),
            anyOf(
                forEachDescendant(
                    memberExpr(isExpansionInMainFile()).bind("fun_memberExpr")),
                unless(forEachDescendant(memberExpr(isExpansionInMainFile())
                                             .bind("fun_memberExpr"))))
            // anyOf(forEachDescendant(parenExpr(isExpansionInMainFile()).bind("fun_parenExpr")),
            // unless(forEachDescendant(parenExpr(isExpansionInMainFile()).bind("fun_parenExpr"))))
            )
            .bind("CXXMethodDecl");

    auto callexpr = callExpr(isExpansionInMainFile()).bind("call_expr");
    auto binaryOperator_ =
        binaryOperator(isExpansionInMainFile()).bind("BinaryOperator");

    auto ifstmt = ifStmt(isExpansionInMainFile()).bind("IfStmt");
    // 如果file的结尾是.h的话
    Finder.addMatcher(decl_matcher, &FuncCall);
    Finder.addMatcher(FuncDeclMatcher, &FuncCall);
    Finder.addMatcher(classMatcher, &FuncCall);
    Finder.addMatcher(MemberCallExpr, &FuncCall);
    Finder.addMatcher(ConstructorDecl, &FuncCall);
    Finder.addMatcher(mmemberExpr, &FuncCall);
    Finder.addMatcher(GlobalVarMatcher, &FuncCall);
    Finder.addMatcher(MethodDecl, &FuncCall);
    Finder.addMatcher(refExpr, &FuncCall);
    Finder.addMatcher(callexpr, &FuncCall);
    Finder.addMatcher(binaryOperator_, &FuncCall);
    Finder.addMatcher(ifstmt, &FuncCall);

    return Finder.newASTConsumer();
  }

private:
  Func_Call FuncCall;
  MatchFinder Finder;
};

string print_class_info() {
  // 输出类信息
  // 类名 基类 虚拟基类 成员变量 成员函数
  string info = "";
  for (int i = 0; i < Class_list.size(); i++) {
    class_Constraint temp_class = Class_list[i];
    // 类名
    info += "{{";
    info += temp_class.class_name + " ## ";
    info += temp_class.start_line + " ## ";
    info += temp_class.end_line + " ## ";
    info += temp_class.type + " ## ";

    // 声明位置
    info += changes(temp_class.decl_loc) + " ## ";
    // 基类
    for (int i = 0; i < temp_class.bases.size(); i++) {
      info += "[";
      info += temp_class.bases[i].class_name + "@@";
      info += temp_class.bases[i].decl_loc + "@@";
      info += temp_class.bases[i].if_virtual + "]";
    }
    info += " ## ";
    // 成员变量
    info += "}{";
    for (int j = 0; j < temp_class.Member_variables.size(); j++) {
      Member_variable m_var = temp_class.Member_variables[j];
      info += "[";
      info += m_var.variable_name + " ;; " + m_var.decl_loc + " ;; " +
              m_var.decl_class + " ;; " + m_var.type_decl_loc + "$$" +
              m_var.type + " ;; " + m_var.authority + "] ;; ";
    }
    info += "} ## ";
    // 成员函数 只输出函数名、声明位置和所在类
    info += "{";
    for (int j = 0; j < temp_class.Functions.size(); j++) {
      Function_Constraint m_fun = temp_class.Functions[j];
      info += "[";
      info += m_fun.function_name + " ;; " + m_fun.function_location + " ;; " +
              m_fun.calss + " ;; " + to_string(m_fun.if_static) + " ;; " +
              to_string(m_fun.if_virtual) + "] ;; ";
    }
    info += "}}\n";
  }
  return info;
}

string print_fun_var_info() {
  // 打印函数变量列表
  string info = "";
  for (int i = 0; i < Function_list.size(); i++) {
    info += Function_list[i].function_name + ";;";
    info += Function_list[i].function_location + ";;";
    for (int j = 0; j < Function_list[i].variables.size(); j++) {
      info += "[";
      info += Function_list[i].variables[j].variable_name + "@@";
      info += Function_list[i].variables[j].type_decl_loc + "$$" +
              Function_list[i].variables[j].type + "@@";
      info += Function_list[i].variables[j].using_loc + "@@";
      info += Function_list[i].variables[j].decl_loc + "@@";
      info += Function_list[i].variables[j].class_decl_loc + "$$" +
              Function_list[i].variables[j].decl_class + "];;";
    }
    info += "\n";
  }

  return info;
}

string print_class_var_info() {
  // 打印函数变量列表
  string info = "";
  for (int i = 0; i < Class_list.size(); i++) {
    info += Class_list[i].class_name + ";;";
    info += changes(Class_list[i].decl_loc) + ";;";
    for (int j = 0; j < Class_list[i].variables.size(); j++) {
      info += "[";
      info += Class_list[i].variables[j].variable_name + "@@"; // 名称
      info += Class_list[i].variables[j].type_decl_loc + "$$" +
              Class_list[i].variables[j].type + "@@";      // 类型
      info += Class_list[i].variables[j].using_loc + "@@"; // 使用位置
      info += Class_list[i].variables[j].decl_loc + "@@";  // 定义位置
      info += Class_list[i].variables[j].class_decl_loc + "$$" +
              Class_list[i].variables[j].decl_class + "];;"; // 类
    }
    info += "\n";
  }

  return info;
}

string print_global_var() {
  // 打印全局变量
  string info = "";
  for (int i = 0; i < global_var.size(); i++) {
    info += global_var[i].name + ";;";
    info += global_var[i].type_decl_loc + "$$" + global_var[i].type + ";;";
    info += global_var[i].decl_loc + "\n";
  }
  return info;
}

string printinfo() {
  string info = "";
  for (int i = 0; i < Function_list.size(); i++) {
    info += "{";
    info += "[" + Function_list[i].function_location + " ;; " +
            Function_list[i].isbody + " ;; " + Function_list[i].function_name +
            " ;; " + Function_list[i].calss + " ;; " +
            to_string(Function_list[i].fun_type) + " ;; " +
            to_string(Function_list[i].if_static) + " ;; " +
            Function_list[i].authority + " ;; " + Function_list[i].start +
            " ;; " + Function_list[i].end + "], ";
    for (int j = 0; j < Function_list[i].call_fun.size(); j++) {
      Call_Fun_Info call_fun = Function_list[i].call_fun[j];
      info += "[" + call_fun.Decl_Loc + " ;; " + call_fun.CallExpr_Loc +
              " ;; " + call_fun.name + "], ";
    }
    info += "}\n\n";
  }
  return info;
}

string printinfo_param() {
  string info = "";

  for (int i = 0; i < Function_list.size(); i++) {

    info += Function_list[i].function_name + ";";
    info += Function_list[i].start + ";";
    info += Function_list[i].end + ";";
    info += Function_list[i].return_type + ";";
    info += Function_list[i].function_location + ";";
    vector<param> params = Function_list[i].params;
    for (int j = 0; j < params.size(); j++) {
      info += params[j].type_decl_loc + "$$" + params[j].type + ";" +
              params[j].name + ";";
    }
    info += "\n";
  }

  return info;
}

string printinfo_param1() {
  string info = "";

  for (int i = 0; i < Function_list.size(); i++) {

    info += Function_list[i].function_name + ";";
    info += Function_list[i].start + ";";
    info += Function_list[i].end + ";";
    info += Function_list[i].return_type + ";";
    info += Function_list[i].function_location + ";";
    for (int j = 0; j < Function_list[i].params.size(); j++) {
      info += "[";
      info += Function_list[i].params[j].name + "@@";
      info += Function_list[i].params[j].type_decl_loc + "$$" +
              Function_list[i].params[j].type + "];;";
    }
    info += "\n";
  }

  return info;
}

string printinfo_name() {
  string info;
  for (int i = 0; i < Function_list.size(); i++) {

    info += Function_list[i].function_location + " " +
            Function_list[i].function_name + " " + Function_list[i].start +
            " " + Function_list[i].end + "\n";
  }
  return info;
}

string printpf_info() {
  string info;
  for (int i = 0; i < pointer_func_list.size(); i++) {
    info += "{";
    info += "[" + pointer_func_list[i].loc + " ;; " +
            pointer_func_list[i].name + "], ";
    for (int j = 0; j < pointer_func_list[i].matched_func_list.size(); j++) {
      pointer_matched_func pmf = pointer_func_list[i].matched_func_list[j];
      info += "[" + pmf.loc + " ;; " + pmf.name + "], ";
    }
    info += "}\n\n";
  }

  return info;
}

string print_ifloc() {
  string info = "";
  for (int i = 0; i < if_loc.size(); i++) {
    info += if_loc[i] + "\n";
  }
  return info;
}

char *strToChar(string strSend) {
  char *ConvertData;
  const int len2 = strSend.length();
  ConvertData = new char[len2 + 1];
  strcpy(ConvertData, strSend.c_str());
  return ConvertData;
}

int main(int argc, const char **argv) {
    ofstream write;
        string file_temp = "";
    //cout << argc << endl;
    for (int i = 1; i < argc; i++)
    {
        //cout << argv[i] << endl;
        string temp;
        temp = argv[i];
        file_temp += temp;
        //cout << file_temp << endl;
    }
    cout << "The file to be analyzed is; " << file_temp << endl;
    char* file = strToChar(file_temp);
    const char* temp[] = { argv[0],file };
    int filenum = 2;
    auto ExpectedParser = CommonOptionsParser::create(filenum, temp, ToolingSampleCategory);
    CommonOptionsParser& op = ExpectedParser.get();
    ClangTool Tool(op.getCompilations(), op.getSourcePathList());

    int result = Tool.run(newFrontendActionFactory<MyFrontendAction>().get());//获得抽象语法树
    //CommonOptionsParser op(argc, argv, ToolingSampleCategory);
    //ClangTool Tool(op.getCompilations(), op.getSourcePathList());

    // ClangTool::run accepts a FrontendActionFactory, which is then used to
    // create new objects implementing the FrontendAction interface. Here we use
    // the helper newFrontendActionFactory to create a default factory that will
    // return a new MyFrontendAction object every time.
    // To further customize this, we could create our own factory class.
    const string filename = temp[1];
    string info_name = "";
    info_name = filename + ".call";
    string info = printinfo();
    write.open(info_name);
    write << info;
    write.close();

    info_name = filename + ".txt";
    string name_s_e = printinfo_name();
    write.open(info_name);
    write << name_s_e;
    write.close();

    info_name = filename + ".parameter";
    string param_info = printinfo_param();
    write.open(info_name);
    write << param_info;
    write.close();

    info_name = filename + ".param";
    string param_info1 = printinfo_param1();
    write.open(info_name);
    write << param_info1;
    write.close();

    info_name = filename + ".success";
    string if_success_info = if_success;
    write.open(info_name);
    write << if_success_info;
    write.close();

    info_name = filename + ".class";
    string class_info = print_class_info();
    write.open(info_name);
    write << class_info;
    write.close();

    info_name = filename + ".var";
    string var_info = print_fun_var_info();
    write.open(info_name);
    write << var_info;
    write.close();

    info_name = filename + ".class_var";
    string class_var_info = print_class_var_info();
    write.open(info_name);
    write << class_var_info;
    write.close();

    info_name = filename + ".gvar";
    string gvar_info = print_global_var();
    write.open(info_name);
    write << gvar_info;
    write.close();

    info_name = filename + ".pf";
    string pf_info = printpf_info();
    write.open(info_name);
    write << pf_info;
    write.close();

    info_name = filename + ".if";
    string if_info = print_ifloc();
    write.open(info_name);
    write << if_info;
    write.close();

    return 0;
}
