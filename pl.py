from antlr4 import *
from antlr4.tree.Trees import Trees

# Importar o parser e lexer para Python gerados pelo ANTLR
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser

# Importar o parser e lexer para Java gerados pelo ANTLR
from JavaLexer import JavaLexer
from JavaParser import JavaParser

def test_code(code, lexer, parser):
    input_stream = InputStream(code)
    lexer = lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = parser(stream)
    tree = parser.compilationUnit()
    print(Trees.toStringTree(tree, None, parser))

# Testar código Python
python_code = """
def hello_world():
    print("Hello, world!")
"""
test_code(python_code, Python3Lexer, Python3Parser)

# Testar código Java
java_code = """
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
"""
#test_code(java_code, JavaLexer, JavaParser)