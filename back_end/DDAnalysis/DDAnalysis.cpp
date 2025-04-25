
#include "clang/AST/AST.h"
#include "clang/AST/ASTConsumer.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/Frontend/ASTConsumers.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
#include "llvm/Support/raw_ostream.h"
#include <llvm/ADT/STLExtras.h>
#include <clang/AST/ASTContext.h>
#include <clang/ASTMatchers/ASTMatchers.h>
#include <clang/ASTMatchers/ASTMatchFinder.h>
#include <fstream>
#include <clang/Frontend/FrontendActions.h>


#include<vector>
#include<string>
#include<map>
#include<set>
#include<unordered_map>
#include<unordered_set>
#include <sstream>
#include <string>

#include"DDAnalysis.h"

using namespace clang;
using namespace clang::driver;
using namespace clang::tooling;
using namespace clang::ast_matchers;

static llvm::cl::OptionCategory ToolingSampleCategory("Tooling Sample");

using namespace std;

typedef struct
{
    string name;
    string CallExpr_Loc;
    string Decl_Loc;
    string return_type;
    string decl_class;
}Call_Fun_Info;

typedef struct
{
    string name;
    string type;
    string type_decl_loc;
    string if_pointer = "0";
}param;

typedef struct
{
    string name;
    string type;
    string type_decl_loc;
    string decl_loc;
}g_var;

typedef struct
{
    string variable_name;
    string decl_loc;
    string using_loc;
    string type;
    string type_decl_loc;
    string decl_class;
    string class_decl_loc;
}var_using;

typedef struct
{
    string function_name; // 方法名
    string function_location; // 声明位置
    string file_path; // 所在文件
    vector<Call_Fun_Info> call_fun; // 调用列表
    string isbody = "1"; // 是否有函数体
    string start; // 起始声明位置
    string end; // 结束声明位置
    string return_type; // 返回类型
    vector<param> params; // 参数列表
    string calss; // 所在类
    vector<var_using> variables; // 变量列表 局部变量+全局变量
    bool if_visual = false;
    int fun_type = 0;
    int if_static = 0;
    int if_virtual = 0;
    string authority;
}Function_Constraint;//方法

typedef struct
{
    string variable_name;
    string decl_loc;
    string type;
    string type_decl_loc;
    string decl_class;
    string if_pointer = "0";
    string authority;

}Member_variable;//成员变量

typedef struct
{
    string class_name;
    string decl_loc;
    string if_virtual = "0";
}class_info;

typedef struct
{
    string class_name;
    string decl_loc;
    vector<class_info> bases;
    vector<string> v_bases;
    vector<Member_variable> Member_variables;
    vector<Function_Constraint> Functions;
    vector<var_using> variables; // 变量列表 局部变量+全局变量
}class_Constraint;//类限制


int fun_count = 1;
vector<var_using> var_using_list;
vector<g_var> var_define_list;
vector<g_var> uop_var_define_list;

string if_success = "1";

//字符串分割函数
std::vector<std::string> split(std::string str, std::string pattern)
{
    std::string::size_type pos;
    std::vector<std::string> result;
    str += pattern;//扩展字符串以方便操作
    int size = str.size();
    for (int i = 0; i < size; i++)
    {
        pos = str.find(pattern, i);
        if (pos < size)
        {
            std::string s = str.substr(i, pos - i);
            result.push_back(s);
            i = pos + pattern.size() - 1;
        }
    }
    return result;
}

string changes(string s)
{
    int pos = 0;
    while ((pos = s.find('\\', pos)) >= 0)
    {
        s.replace(pos, 1, "/");
        //也可以多插入一个\来达成
        //input.insert(pos, "\\");
        pos += 1;
    }
    return s;
}

DeclRefExpr* get_DeclRefExpr(MemberExpr* memberExpr)
{
    string type = memberExpr->getType().getAsString();

    if (type == "<bound member function type>" || (type.find("(") != string::npos && type.find(")") != string::npos))
    {
        //cout << "pass" << endl;
    }
    else
    {
        if (isa<ImplicitCastExpr>(memberExpr->getBase()))
        {
            if (isa<DeclRefExpr>(cast<ImplicitCastExpr>(memberExpr->getBase())->getSubExpr()))
            {
                return cast<DeclRefExpr>(cast<ImplicitCastExpr>(memberExpr->getBase())->getSubExpr());
            }
            else if (isa<MemberExpr>(cast<ImplicitCastExpr>(memberExpr->getBase())->getSubExpr()))
            {
                return get_DeclRefExpr(cast<MemberExpr>(cast<ImplicitCastExpr>(memberExpr->getBase())->getSubExpr()));
            }
        }
        else if (isa<DeclRefExpr>(memberExpr->getBase()))
        {
            return cast<DeclRefExpr>(memberExpr->getBase());
        }
        else if (isa<ArraySubscriptExpr>(memberExpr->getBase()))
        {
            auto temp = cast<ArraySubscriptExpr>(memberExpr->getBase())->getBase();
            if (isa<ImplicitCastExpr>(temp))
            {
                auto temp1 = cast<ImplicitCastExpr>(temp)->getSubExpr();
                if (isa<DeclRefExpr>(temp1))
                {
                    return cast<DeclRefExpr>(temp1);
                }

                if (isa<MemberExpr>(temp1))
                {
                    return get_DeclRefExpr(cast<MemberExpr>(temp1));
                }
            }
        }

    }

    return NULL;

}

class Func_Call : public MatchFinder::MatchCallback
{
public:
    //Func_Call(ASTContext* astContext) : astContext(astContext) {}
    void run(const MatchFinder::MatchResult& Result) override
    {
        string functionname;
        clang::LangOptions LangOpts;
        LangOpts.CPlusPlus = true;
        clang::PrintingPolicy Policy(LangOpts); //指定标志为c++ 模式，用于从expr 获取类型字符串
        if (auto const* declRef = Result.Nodes.getNodeAs<DeclRefExpr>("declRefExpr"))
        {
            //cout << "变量使用DeclRefExpr" << endl;
            auto func = declRef->getDecl();
            auto type = declRef->getType().getAsString();
            if (!isa<FunctionDecl>(func))
            {
                string var_type = func->getType().getAsString();
                string type_decl_loc = "";
                if (func->getType()->getAsCXXRecordDecl() != NULL)
                    type_decl_loc = func->getType()->getAsCXXRecordDecl()->getBeginLoc().printToString(Result.Context->getSourceManager());
                string var_name = func->getNameAsString();
                string var_decl_loc = func->getBeginLoc().printToString(Result.Context->getSourceManager());
                var_decl_loc = changes(var_decl_loc);
                string var_using_loc = declRef->getBeginLoc().printToString(Result.Context->getSourceManager());
                var_using_loc = changes(var_using_loc);

                var_using new_used_var;
                new_used_var.variable_name = var_name;
                new_used_var.type = var_type;
                new_used_var.type_decl_loc = changes(type_decl_loc);
                new_used_var.decl_loc = var_decl_loc;
                new_used_var.using_loc = var_using_loc;
                var_using_list.push_back(new_used_var);
            }

        }
        if (auto const* varDecl = Result.Nodes.getNodeAs<VarDecl>("varDecl"))
        {
            //cout << "变量声明VarDecl" << endl;
            string var_name = varDecl->getNameAsString();
            string var_type = varDecl->getType().getAsString();
            string type_decl_loc = "";
            if (varDecl->getType()->getAsCXXRecordDecl() != NULL)
                type_decl_loc = varDecl->getType()->getAsCXXRecordDecl()->getBeginLoc().printToString(Result.Context->getSourceManager());
            string decl_loc = varDecl->getBeginLoc().printToString(Result.Context->getSourceManager());
            g_var new_g_var;
            new_g_var.name = var_name;
            new_g_var.type = var_type;
            new_g_var.type_decl_loc = changes(type_decl_loc);
            new_g_var.decl_loc = changes(decl_loc);
            var_define_list.push_back(new_g_var);
        }
        if (auto const* binaryOperator = Result.Nodes.getNodeAs<BinaryOperator>("binaryOperator"))
        {
            //cout << "二元操作符" << endl;
            // 通过二元操作符寻找函数指针赋值
            string Opp = binaryOperator->getOpcodeStr().data();
            Expr* binaryOperator_left = binaryOperator->getLHS();
            if (isa<DeclRefExpr>(binaryOperator_left) && (Opp == "=" || Opp == "+=" || Opp == "-=" || Opp == "*=" || Opp == "/=" || Opp == "%=" || Opp == "|=" || Opp == "&="))
            {
                auto declRef = cast<DeclRefExpr>(binaryOperator_left);
                auto func = declRef->getDecl();
                auto type = declRef->getType().getAsString();
                if (!isa<FunctionDecl>(func))
                {
                    string var_type = func->getType().getAsString();
                    string type_decl_loc = "";
                    if (func->getType()->getAsCXXRecordDecl() != NULL)
                        type_decl_loc = func->getType()->getAsCXXRecordDecl()->getBeginLoc().printToString(Result.Context->getSourceManager());
                    string var_name = func->getNameAsString();
                    string var_decl_loc = func->getBeginLoc().printToString(Result.Context->getSourceManager());
                    var_decl_loc = changes(var_decl_loc);
                    string var_using_loc = declRef->getBeginLoc().printToString(Result.Context->getSourceManager());
                    var_using_loc = changes(var_using_loc);

                    g_var new_used_var;
                    new_used_var.name = var_name;
                    new_used_var.type = var_type;
                    new_used_var.type_decl_loc = changes(type_decl_loc);
                    new_used_var.decl_loc = var_using_loc;
                    if (Opp == "+=" || Opp == "-=" || Opp == "*=" || Opp == "/=" || Opp == "%=" || Opp == "|=" || Opp == "&=")
                        uop_var_define_list.push_back(new_used_var);
                    else
                        var_define_list.push_back(new_used_var);
                }
            }

            if (isa<MemberExpr>(binaryOperator_left) && (Opp == "=" || Opp == "+=" || Opp == "-=" || Opp == "*=" || Opp == "/=" || Opp == "%=" || Opp == "|=" || Opp == "&="))
            {
                //cout << "MemberExpr" << endl;
                MemberExpr* memberExpr = cast<MemberExpr>(binaryOperator_left);
                //cout << cast<MemberExpr>(binaryOperator_left)->getBeginLoc().printToString(Result.Context->getSourceManager()) << endl;
                string type = memberExpr->getType().getAsString();

                if (type == "<bound member function type>" || (type.find("(") != string::npos && type.find(")") != string::npos))
                {
                    ////cout << "pass" << endl;
                }
                else
                {   
                    auto declRef = get_DeclRefExpr(memberExpr);
                    /*if (isa<ImplicitCastExpr>(memberExpr->getBase()))
                    {
                        if (isa<DeclRefExpr>(cast<ImplicitCastExpr>(memberExpr->getBase())->getSubExpr()))
                        {
                            auto declRef = cast<DeclRefExpr>(cast<ImplicitCastExpr>(memberExpr->getBase())->getSubExpr());
                            auto func = declRef->getDecl();
                            auto type = declRef->getType().getAsString();
                            if (!isa<FunctionDecl>(func))
                            {
                                string var_type = func->getType().getAsString();
                                string type_decl_loc = "";
                                if (func->getType()->getAsCXXRecordDecl() != NULL)
                                    type_decl_loc = func->getType()->getAsCXXRecordDecl()->getBeginLoc().printToString(Result.Context->getSourceManager());
                                string var_name = func->getNameAsString();
                                string var_decl_loc = func->getBeginLoc().printToString(Result.Context->getSourceManager());
                                var_decl_loc = changes(var_decl_loc);
                                string var_using_loc = declRef->getBeginLoc().printToString(Result.Context->getSourceManager());
                                var_using_loc = changes(var_using_loc);

                                g_var new_used_var;
                                new_used_var.name = var_name;
                                new_used_var.type = var_type;
                                new_used_var.type_decl_loc = changes(type_decl_loc);
                                new_used_var.decl_loc = var_using_loc;
                                var_define_list.push_back(new_used_var);
                            }
                        }
                    }
                    else if (isa<DeclRefExpr>(memberExpr->getBase()))
                    {*/
                        //auto declRef = cast<DeclRefExpr>(memberExpr->getBase());
                    if (declRef != NULL)
                    {
                        if (isa<DeclRefExpr>(declRef))
                        {
                            auto func = declRef->getDecl();
                            auto type = declRef->getType().getAsString();
                            if (!isa<FunctionDecl>(func))
                            {
                                string var_type = func->getType().getAsString();
                                string type_decl_loc = "";
                                if (func->getType()->getAsCXXRecordDecl() != NULL)
                                    type_decl_loc = func->getType()->getAsCXXRecordDecl()->getBeginLoc().printToString(Result.Context->getSourceManager());
                                string var_name = func->getNameAsString();
                                string var_decl_loc = func->getBeginLoc().printToString(Result.Context->getSourceManager());
                                var_decl_loc = changes(var_decl_loc);
                                string var_using_loc = declRef->getBeginLoc().printToString(Result.Context->getSourceManager());
                                var_using_loc = changes(var_using_loc);

                                g_var new_used_var;
                                new_used_var.name = var_name;
                                new_used_var.type = var_type;
                                new_used_var.type_decl_loc = changes(type_decl_loc);
                                new_used_var.decl_loc = var_using_loc;
                                //var_define_list.push_back(new_used_var);

                                if (Opp == "+=" || Opp == "-=" || Opp == "*=" || Opp == "/=" || Opp == "%=" || Opp == "|=" || Opp == "&=")
                                    uop_var_define_list.push_back(new_used_var);
                                else
                                    var_define_list.push_back(new_used_var);
                            }
                        }
                    }
                    else
                    {
                        if (isa<ParenExpr>(memberExpr->getBase()))
                        {
                            auto paren = cast<ParenExpr>(memberExpr->getBase());
                            string begin_loc = paren->getBeginLoc().printToString(Result.Context->getSourceManager());
                            begin_loc = changes(begin_loc);
                            string end_loc = paren->getEndLoc().printToString(Result.Context->getSourceManager());
                            end_loc = changes(end_loc);
                            //using_loc = 
                            string var_name = begin_loc;
                            string var_decl_loc = begin_loc;
                            string var_using_loc = begin_loc;
                            string var_type = paren->getType().getAsString();
                            g_var new_used_var;
                            new_used_var.name = var_name;
                            new_used_var.type = var_type;
                            new_used_var.type_decl_loc = "";
                            new_used_var.decl_loc = var_using_loc;
                            //var_define_list.push_back(new_used_var);

                            if (Opp == "+=" || Opp == "-=" || Opp == "*=" || Opp == "/=" || Opp == "%=" || Opp == "|=" || Opp == "&=")
                                uop_var_define_list.push_back(new_used_var);
                            else
                                var_define_list.push_back(new_used_var);
                            //cout << begin_loc << endl;
                        }
                    }
                    //}
                }
            }

            if (isa<ArraySubscriptExpr>(binaryOperator_left) && (Opp == "=" || Opp == "+=" || Opp == "-=" || Opp == "*=" || Opp == "/=" || Opp == "%=" || Opp == "|=" || Opp == "&="))
            {
                auto temp = cast<ArraySubscriptExpr>(binaryOperator_left)->getBase();
                if (isa<ImplicitCastExpr>(temp))
                {
                    auto temp1 = cast<ImplicitCastExpr>(temp)->getSubExpr();
                    if (isa<DeclRefExpr>(temp1))
                    {
                        auto declRef = cast<DeclRefExpr>(temp1);
                        auto func = declRef->getDecl();
                        auto type = declRef->getType().getAsString();
                        if (!isa<FunctionDecl>(func))
                        {
                            string var_type = func->getType().getAsString();
                            string type_decl_loc = "";
                            if (func->getType()->getAsCXXRecordDecl() != NULL)
                                type_decl_loc = func->getType()->getAsCXXRecordDecl()->getBeginLoc().printToString(Result.Context->getSourceManager());
                            string var_name = func->getNameAsString();
                            string var_decl_loc = func->getBeginLoc().printToString(Result.Context->getSourceManager());
                            var_decl_loc = changes(var_decl_loc);
                            string var_using_loc = declRef->getBeginLoc().printToString(Result.Context->getSourceManager());
                            var_using_loc = changes(var_using_loc);

                            g_var new_used_var;
                            new_used_var.name = var_name;
                            new_used_var.type = var_type;
                            new_used_var.type_decl_loc = changes(type_decl_loc);
                            new_used_var.decl_loc = var_using_loc;
                            if (Opp == "+=" || Opp == "-=" || Opp == "*=" || Opp == "/=" || Opp == "%=" || Opp == "|=" || Opp == "&=")
                                uop_var_define_list.push_back(new_used_var);
                            else
                                var_define_list.push_back(new_used_var);
                        }
                    }

                    if (isa<MemberExpr>(temp1))
                    {
                        //cout << "MemberExpr" << endl;
                        auto memberExpr = cast<MemberExpr>(temp1);
                        //cout << cast<MemberExpr>(temp1)->getBeginLoc().printToString(Result.Context->getSourceManager()) << endl;
                        string type = memberExpr->getType().getAsString();

                        if (type == "<bound member function type>" || (type.find("(") != string::npos && type.find(")") != string::npos))
                        {
                            ////cout << "pass" << endl;
                        }
                        else
                        {
                            auto declRef = get_DeclRefExpr(memberExpr);
                            if (declRef != NULL)
                            {
                                if (isa<DeclRefExpr>(declRef))
                                {
                                    auto func = declRef->getDecl();
                                    auto type = declRef->getType().getAsString();
                                    if (!isa<FunctionDecl>(func))
                                    {
                                        string var_type = func->getType().getAsString();
                                        string type_decl_loc = "";
                                        if (func->getType()->getAsCXXRecordDecl() != NULL)
                                            type_decl_loc = func->getType()->getAsCXXRecordDecl()->getBeginLoc().printToString(Result.Context->getSourceManager());
                                        string var_name = func->getNameAsString();
                                        string var_decl_loc = func->getBeginLoc().printToString(Result.Context->getSourceManager());
                                        var_decl_loc = changes(var_decl_loc);
                                        string var_using_loc = declRef->getBeginLoc().printToString(Result.Context->getSourceManager());
                                        var_using_loc = changes(var_using_loc);

                                        g_var new_used_var;
                                        new_used_var.name = var_name;
                                        new_used_var.type = var_type;
                                        new_used_var.type_decl_loc = changes(type_decl_loc);
                                        new_used_var.decl_loc = var_using_loc;
                                        if (Opp == "+=" || Opp == "-=" || Opp == "*=" || Opp == "/=" || Opp == "%=" || Opp == "|=" || Opp == "&=")
                                            uop_var_define_list.push_back(new_used_var);
                                        else
                                            var_define_list.push_back(new_used_var);
                                    }
                                }
                            }
                        }
                    }
                }
            }

        }

        if (auto const* varDecl = Result.Nodes.getNodeAs<ParenExpr>("parenExpr"))
        {
            auto paren = varDecl;
            string begin_loc = paren->getBeginLoc().printToString(Result.Context->getSourceManager());
            begin_loc = changes(begin_loc);
            string end_loc = paren->getEndLoc().printToString(Result.Context->getSourceManager());
            end_loc = changes(end_loc);
            //using_loc = 
            string var_name = begin_loc;
            string var_decl_loc = begin_loc;
            string var_using_loc = begin_loc;
            string var_type = paren->getType().getAsString();

            var_using new_used_var;
            new_used_var.variable_name = var_name;
            new_used_var.type = var_type;
            new_used_var.type_decl_loc = "";
            new_used_var.decl_loc = var_decl_loc;
            new_used_var.using_loc = var_using_loc;
            var_using_list.push_back(new_used_var);
        }
        if (auto const* varDecl = Result.Nodes.getNodeAs<UnaryOperator>("unaryOperator"))
        {
            //cout << "一元操作符" << endl;
            string OP = varDecl->getOpcodeStr(varDecl->getOpcode()).data();
            if (OP == "++" || OP == "--")
            {
                Expr* FS_Inc_UO_Sub = varDecl->getSubExpr();
                
                if (FS_Inc_UO_Sub != NULL && isa<DeclRefExpr>(FS_Inc_UO_Sub))
                {
                    auto declRef = cast<DeclRefExpr>(FS_Inc_UO_Sub);
                    auto func = declRef->getDecl();
                    auto type = declRef->getType().getAsString();
                    if (!isa<FunctionDecl>(func))
                    {
                        string var_type = func->getType().getAsString();
                        string type_decl_loc = "";
                        if (func->getType()->getAsCXXRecordDecl() != NULL)
                            type_decl_loc = func->getType()->getAsCXXRecordDecl()->getBeginLoc().printToString(Result.Context->getSourceManager());
                        string var_name = func->getNameAsString();
                        string var_decl_loc = func->getBeginLoc().printToString(Result.Context->getSourceManager());
                        var_decl_loc = changes(var_decl_loc);
                        string var_using_loc = declRef->getBeginLoc().printToString(Result.Context->getSourceManager());
                        var_using_loc = changes(var_using_loc);

                        g_var new_used_var;
                        new_used_var.name = var_name;
                        new_used_var.type = var_type;
                        new_used_var.type_decl_loc = changes(type_decl_loc);
                        new_used_var.decl_loc = var_using_loc;
                        uop_var_define_list.push_back(new_used_var);
                    }
                }
                else if (FS_Inc_UO_Sub != NULL && isa<ParenExpr>(FS_Inc_UO_Sub))
                {
                    auto subExpr = cast<ParenExpr>(FS_Inc_UO_Sub)->getSubExpr();
                    if (subExpr != NULL && isa<UnaryOperator>(subExpr))
                    {
                        string subOP = cast<UnaryOperator>(subExpr)->getOpcodeStr(cast<UnaryOperator>(subExpr)->getOpcode()).data();
                        if (subOP == "*")
                        {
                            subExpr = cast<UnaryOperator>(subExpr)->getSubExpr();
                            if (subExpr != NULL && isa<ImplicitCastExpr>(subExpr))
                            {
                                subExpr = cast<ImplicitCastExpr>(subExpr)->getSubExpr();
                                if (subExpr != NULL && isa<DeclRefExpr>(subExpr))
                                {
                                    auto declRef = cast<DeclRefExpr>(subExpr);
                                    auto func = declRef->getDecl();
                                    auto type = declRef->getType().getAsString();
                                    if (!isa<FunctionDecl>(func))
                                    {
                                        string var_type = func->getType().getAsString();
                                        string type_decl_loc = "";
                                        if (func->getType()->getAsCXXRecordDecl() != NULL)
                                            type_decl_loc = func->getType()->getAsCXXRecordDecl()->getBeginLoc().printToString(Result.Context->getSourceManager());
                                        string var_name = func->getNameAsString();
                                        string var_decl_loc = func->getBeginLoc().printToString(Result.Context->getSourceManager());
                                        var_decl_loc = changes(var_decl_loc);
                                        string var_using_loc = declRef->getBeginLoc().printToString(Result.Context->getSourceManager());
                                        var_using_loc = changes(var_using_loc);

                                        g_var new_used_var;
                                        new_used_var.name = var_name;
                                        new_used_var.type = var_type;
                                        new_used_var.type_decl_loc = changes(type_decl_loc);
                                        new_used_var.decl_loc = var_using_loc;
                                        uop_var_define_list.push_back(new_used_var);
                                    }
                                }

                            }
                        }
                    }
                    
                }
            }

        }
        // 如果解析成功的话
        if_success = "0";

        return;
    }
};

class MyFrontendAction : public ASTFrontendAction
{
public:
    MyFrontendAction() = default;
    void EndSourceFileAction() override
    {
        auto m = getCompilerInstance().getDiagnostics().getNumWarnings();
        //spdlog::info("{} Warning\n", m);
    }
    unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance& CI, StringRef file) override
    {
        llvm::errs() << "** Creating AST consumer for: " << file << "\n";
        auto m = CI.getDiagnostics().getNumWarnings();
        //spdlog::info("{}", m);
        /*auto decl_matcher = decl(isExpansionInMainFile(), hasDeclContext(translationUnitDecl())
        ).bind("Decl_node");*/

        auto decl_matcher = translationUnitDecl().bind("TranslationUnitDecl");


        auto refExpr = declRefExpr(isExpansionInMainFile()).bind("declRefExpr");// 变量使用
        auto vardecl = varDecl(isExpansionInMainFile()).bind("varDecl");// 变量声明
        auto fielddecl = fieldDecl(isExpansionInMainFile()).bind("fieldDecl");// 成员变量声明
        auto BinaryOp = binaryOperator(isExpansionInMainFile()).bind("binaryOperator");// 二元操作符
        auto UnaryOp = unaryOperator(isExpansionInMainFile()).bind("unaryOperator");// 一元操作符

        auto Paren = parenExpr(isExpansionInMainFile()).bind("parenExpr");// 宏定义


        // 如果file的结尾是.h的话
        Finder.addMatcher(decl_matcher, &FuncCall);
        Finder.addMatcher(refExpr, &FuncCall);
        Finder.addMatcher(vardecl, &FuncCall);
        Finder.addMatcher(fielddecl, &FuncCall);

        Finder.addMatcher(BinaryOp, &FuncCall);
        Finder.addMatcher(UnaryOp, &FuncCall);
        Finder.addMatcher(Paren, &FuncCall);
        return Finder.newASTConsumer();
    }

private:
    Func_Call FuncCall;
    MatchFinder Finder;
};

string print_var_using()
{
    string info = "";
    for (int i = 0; i < var_using_list.size(); i++)
    {
        info += var_using_list[i].variable_name + ";;";
        info += var_using_list[i].type_decl_loc + "$$" + var_using_list[i].type + ";;";
        info += var_using_list[i].using_loc + ";;";
        info += var_using_list[i].decl_loc + "\n";
    }
    return info;
}

string print_var_define1()
{
    string info = "";
    for (int i = 0; i < var_define_list.size(); i++)
    {
        info += var_define_list[i].name + ";;";
        info += var_define_list[i].type_decl_loc + "$$" + var_define_list[i].type + ";;";
        info += var_define_list[i].decl_loc + "\n";
    }
    return info;
}

string print_var_define2()
{
    string info = "";
    for (int i = 0; i < uop_var_define_list.size(); i++)
    {
        info += uop_var_define_list[i].name + ";;";
        info += uop_var_define_list[i].type_decl_loc + "$$" + uop_var_define_list[i].type + ";;";
        info += uop_var_define_list[i].decl_loc + "\n";
    }
    return info;
}

char* strToChar(string strSend)
{
    char* ConvertData;
    const int len2 = strSend.length();
    ConvertData = new char[len2 + 1];
    strcpy(ConvertData, strSend.c_str());
    return ConvertData;
}
int main(int argc, const char** argv)
{
    ofstream write;
    //_set_abort_behavior(0, _WRITE_ABORT_MSG);
    //const char* temp[] = { "BuildCG.exe", "E:\\PYCODE\\design_re_0405\\CUnit_dr\\code\\Headers\\CUnit_intl.h"};
    //const char* temp[] = { "DDAnalysis.exe","E:/C_master/dev1020/C_Quality_Evaluator/app/test/code/User/USER/system_stm32f4xx.c" };
    string file_temp = "";
    //cout << argc << endl;
    for (int i = 1; i < argc; i++)
    {
        //cout << argv[i] << endl;
        string temp;
        temp = argv[i];
        file_temp += " ";
        file_temp += temp;
        //cout << file_temp << endl;
    }
    file_temp.erase(file_temp.begin());
    cout << "The file to be analyzed is; " << file_temp << endl;
    char* file = strToChar(file_temp);
    const char* temp[] = { argv[0],file };
    int filenum = 2;
    auto ExpectedParser = CommonOptionsParser::create(filenum, temp, ToolingSampleCategory);
    CommonOptionsParser& op = ExpectedParser.get();
    ClangTool Tool(op.getCompilations(), op.getSourcePathList());

    int result = Tool.run(newFrontendActionFactory<MyFrontendAction>().get());//获得抽象语法树
    const string filename = temp[1];
    string info_name = "";
    info_name = filename + ".var_using";
    string name_s_e = print_var_using();
    write.open(info_name);
    write << name_s_e;
    write.close();

    info_name = filename + ".var_define1";
    string param_info = print_var_define1();
    write.open(info_name);
    write << param_info;
    write.close();

    info_name = filename + ".var_define2";
    string param_info1 = print_var_define2();
    write.open(info_name);
    write << param_info1;
    write.close();
    return 0;
}

