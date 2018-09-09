
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class CompilationEngine {

    private PrintWriter printWriter;
    private PrintWriter tokenPrintWriter;
    private JackTokenizer tokenizer;

    //Creamos el CompilationEngine con la entrada inFile y salidas outFile, outTokenFile
    public CompilationEngine(File inFile, File outFile, File outTokenFile) {

        try {

            tokenizer = new JackTokenizer(inFile);
            printWriter = new PrintWriter(outFile);
            tokenPrintWriter = new PrintWriter(outTokenFile);

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

    }

    //Compila el tipo de token

    private void compileType(){

        tokenizer.advance();

        boolean isType = false;

        if (tokenizer.tokenType() == JackTokenizer.KEYWORD && (tokenizer.keyWord() == JackTokenizer.INT || tokenizer.keyWord() == JackTokenizer.CHAR || tokenizer.keyWord() == JackTokenizer.BOOLEAN)){
            printWriter.print("<keyword>" + tokenizer.getCurrentToken() + "</keyword>\n");
            tokenPrintWriter.print("<keyword>" + tokenizer.getCurrentToken() + "</keyword>\n");
            isType = true;
        }

        if (tokenizer.tokenType() == JackTokenizer.IDENTIFIER){
            printWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
            tokenPrintWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
            isType = true;
        }

        if (!isType) error("in|char|boolean|className");
    }

    //Compila: 'class' className '{' classVarDec* subroutineDec* '}'

    public void compileClass(){

        //'class'
        tokenizer.advance();

        if (tokenizer.tokenType() != JackTokenizer.KEYWORD || tokenizer.keyWord() != JackTokenizer.CLASS){
            error("class");
        }

        printWriter.print("<class>\n");
        tokenPrintWriter.print("<tokens>\n");

        printWriter.print("<keyword>class</keyword>\n");
        tokenPrintWriter.print("<keyword>class</keyword>\n");

        //className
        tokenizer.advance();

        if (tokenizer.tokenType() != JackTokenizer.IDENTIFIER){
            error("className");
        }

        printWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
        tokenPrintWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");

        //'{'
        requireSymbol('{');

        //classVarDec* subroutineDec*
        compileClassVarDec();
        compileSubroutine();

        //'}'
        requireSymbol('}');

        if (tokenizer.hasMoreTokens()){
            throw new IllegalStateException("Unexpected tokens");
        }

        tokenPrintWriter.print("</tokens>\n");
        printWriter.print("</class>\n");

        //guarda el archivo
        printWriter.close();
        tokenPrintWriter.close();

    }

    //clase: 'class' className '{' classVarDec * subroutineDec * '}'
    private void compileClassVarDec(){
        tokenizer.advance();

        //Mira si el siguiente es un '}'
        if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == '}'){
            tokenizer.pointerBack();
            return;
        }

        //next is start subroutineDec or classVarDec, both start with keyword
        if (tokenizer.tokenType() != JackTokenizer.KEYWORD){
            error("Keywords");
        }

        //siguiente es una subroutineDec
        if (tokenizer.keyWord() == JackTokenizer.CONSTRUCTOR || tokenizer.keyWord() == JackTokenizer.FUNCTION || tokenizer.keyWord() == JackTokenizer.METHOD){
            tokenizer.pointerBack();
            return;
        }

        printWriter.print("<classVarDec>\n");

        //classVarDec existe
        if (tokenizer.keyWord() != JackTokenizer.STATIC && tokenizer.keyWord() != JackTokenizer.FIELD){
            error("static or field");
        }

        printWriter.print("<keyword>" + tokenizer.getCurrentToken() + "</keyword>\n");
        tokenPrintWriter.print("<keyword>" + tokenizer.getCurrentToken() + "</keyword>\n");

        //type
        compileType();

        boolean varNamesDone = false;

        do {

            //varName
            tokenizer.advance();
            if (tokenizer.tokenType() != JackTokenizer.IDENTIFIER){
                error("identifier");
            }

            printWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
            tokenPrintWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");

            //',' o ';'
            tokenizer.advance();

            if (tokenizer.tokenType() != JackTokenizer.SYMBOL || (tokenizer.symbol() != ',' && tokenizer.symbol() != ';')){
                error("',' or ';'");
            }

            if (tokenizer.symbol() == ','){

                printWriter.print("<symbol>,</symbol>\n");
                tokenPrintWriter.print("<symbol>,</symbol>\n");

            }else {

                printWriter.print("<symbol>;</symbol>\n");
                tokenPrintWriter.print("<symbol>;</symbol>\n");
                break;
            }


        }while(true);

        printWriter.print("</classVarDec>\n");

        compileClassVarDec();
    }

    //Compiles a complete method,function, or constructor.
    private void compileSubroutine(){

        tokenizer.advance();

        //siguiente debe es un '}'
        if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == '}'){
            tokenizer.pointerBack();
            return;
        }

        if (tokenizer.tokenType() != JackTokenizer.KEYWORD || (tokenizer.keyWord() != JackTokenizer.CONSTRUCTOR && tokenizer.keyWord() != JackTokenizer.FUNCTION && tokenizer.keyWord() != JackTokenizer.METHOD)){
            error("constructor|function|method");
        }

        printWriter.print("<subroutineDec>\n");

        printWriter.print("<keyword>" + tokenizer.getCurrentToken() + "</keyword>\n");
        tokenPrintWriter.print("<keyword>" + tokenizer.getCurrentToken() + "</keyword>\n");

        //'void' o type
        tokenizer.advance();
        if (tokenizer.tokenType() == JackTokenizer.KEYWORD && tokenizer.keyWord() == JackTokenizer.VOID){
            printWriter.print("<keyword>void</keyword>\n");
            tokenPrintWriter.print("<keyword>void</keyword>\n");
        }else {
            tokenizer.pointerBack();
            compileType();
        }

        //subroutineName which is a identifier
        tokenizer.advance();
        if (tokenizer.tokenType() != JackTokenizer.IDENTIFIER){
            error("subroutineName");
        }

        printWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
        tokenPrintWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");

        //'('
        requireSymbol('(');

        //parameterList
        printWriter.print("<parameterList>\n");
        compileParameterList();
        printWriter.print("</parameterList>\n");

        //')'
        requireSymbol(')');

        //subroutineBody
        compileSubroutineBody();

        printWriter.print("</subroutineDec>\n");

        compileSubroutine();

    }

    //Compila el cuerpo de una subrutina
    private void compileSubroutineBody(){
        printWriter.print("<subroutineBody>\n");
        //'{'
        requireSymbol('{');
        //varDec*
        compileVarDec();
        //statements
        printWriter.print("<statements>\n");
        compileStatement();
        printWriter.print("</statements>\n");
        //'}'
        requireSymbol('}');
        printWriter.print("</subroutineBody>\n");
    }


    private void compileStatement(){

      //determine whether there is a statementnext can be a '}'
        tokenizer.advance();

        //siguiente '}'
        if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == '}'){
            tokenizer.pointerBack();
            return;
        }

        //siguiente caso 'let'|'if'|'while'|'do'|'return'
        if (tokenizer.tokenType() != JackTokenizer.KEYWORD){
            error("keyword");
        }else {
            switch (tokenizer.keyWord()){
                case JackTokenizer.LET:compileLet();break;
                case JackTokenizer.IF:compileIf();break;
                case JackTokenizer.WHILE:compilesWhile();break;
                case JackTokenizer.DO:compileDo();break;
                case JackTokenizer.RETURN:compileReturn();break;
                default:error("'let'|'if'|'while'|'do'|'return'");
            }
        }

        compileStatement();
    }

    /**
     * Compila a (possibly empty) lista de paramentro
     * ((type varName)(',' type varName)*)?
     */
    private void compileParameterList(){

        //check if there is parameterList, if next token is ')' than go back
        tokenizer.advance();
        if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == ')'){
            tokenizer.pointerBack();
            return;
        }

        //there is parameter, at least one varName
        tokenizer.pointerBack();
        do {
            //type
            compileType();

            //varName
            tokenizer.advance();
            if (tokenizer.tokenType() != JackTokenizer.IDENTIFIER){
                error("identifier");
            }
             printWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
            tokenPrintWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");

            //',' o ')'
            tokenizer.advance();
            if (tokenizer.tokenType() != JackTokenizer.SYMBOL || (tokenizer.symbol() != ',' && tokenizer.symbol() != ')')){
                error("',' or ')'");
            }

            if (tokenizer.symbol() == ','){
                printWriter.print("<symbol>,</symbol>\n");
                tokenPrintWriter.print("<symbol>,</symbol>\n");
            }else {
                tokenizer.pointerBack();
                break;
            }

        }while(true);

    }

    /**
     * Compila una var declaration
     */
    private void compileVarDec(){

        //determina if es un varDec

        tokenizer.advance();
        //no 'var' vuelve atras
        if (tokenizer.tokenType() != JackTokenizer.KEYWORD || tokenizer.keyWord() != JackTokenizer.VAR){
            tokenizer.pointerBack();
            return;
        }

        printWriter.print("<varDec>\n");

        printWriter.print("<keyword>var</keyword>\n");
        tokenPrintWriter.print("<keyword>var</keyword>\n");

        //type
        compileType();

        boolean varNamesDone = false;

        do {

            //varName
            tokenizer.advance();

            if (tokenizer.tokenType() != JackTokenizer.IDENTIFIER){
                error("identifier");
            }

            printWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
            tokenPrintWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");

            //',' o ';'
            tokenizer.advance();

            if (tokenizer.tokenType() != JackTokenizer.SYMBOL || (tokenizer.symbol() != ',' && tokenizer.symbol() != ';')){
                error("',' or ';'");
            }

            if (tokenizer.symbol() == ','){

                printWriter.print("<symbol>,</symbol>\n");
                tokenPrintWriter.print("<symbol>,</symbol>\n");

            }else {

                printWriter.print("<symbol>;</symbol>\n");
                tokenPrintWriter.print("<symbol>;</symbol>\n");
                break;
            }


        }while(true);

        printWriter.print("</varDec>\n");

        compileVarDec();

    }

    //Compila un statement
    private void compileDo(){
        printWriter.print("<doStatement>\n");

        printWriter.print("<keyword>do</keyword>\n");
        tokenPrintWriter.print("<keyword>do</keyword>\n");

        compileSubroutineCall();
        //';'
        requireSymbol(';');

        printWriter.print("</doStatement>\n");
    }

    /**
     * Compila un let statement
     * 'let' varName ('[' ']')? '=' expression ';'
     */
    private void compileLet(){

        printWriter.print("<letStatement>\n");

        printWriter.print("<keyword>let</keyword>\n");
        tokenPrintWriter.print("<keyword>let</keyword>\n");

        //varName
        tokenizer.advance();
        if (tokenizer.tokenType() != JackTokenizer.IDENTIFIER){
            error("varName");
        }

        printWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
        tokenPrintWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");

        //'[' o '='
        tokenizer.advance();
        if (tokenizer.tokenType() != JackTokenizer.SYMBOL || (tokenizer.symbol() != '[' && tokenizer.symbol() != '=')){
            error("'['|'='");
        }

        boolean expExist = false;

        //'[' expression ']'
        if (tokenizer.symbol() == '['){

            expExist = true;

            printWriter.print("<symbol>[</symbol>\n");
            tokenPrintWriter.print("<symbol>[</symbol>\n");

            compileExpression();

            //']'
            tokenizer.advance();
            if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == ']'){
                printWriter.print("<symbol>]</symbol>\n");
                tokenPrintWriter.print("<symbol>]</symbol>\n");
            }else {
                error("']'");
            }
        }

        if (expExist) tokenizer.advance();

        //'='
        printWriter.print("<symbol>=</symbol>\n");
        tokenPrintWriter.print("<symbol>=</symbol>\n");

        //expression
        compileExpression();

        //';'
        requireSymbol(';');

        printWriter.print("</letStatement>\n");
    }

    /**
     * Compila mientras (' expression ')' '{' statements '}'
     */
    private void compilesWhile(){
        printWriter.print("<whileStatement>\n");

        printWriter.print("<keyword>while</keyword>\n");
        tokenPrintWriter.print("<keyword>while</keyword>\n");
        //'('
        requireSymbol('(');
        //expression
        compileExpression();
        //')'
        requireSymbol(')');
        //'{'
        requireSymbol('{');
        //statements
        printWriter.print("<statements>\n");
        compileStatement();
        printWriter.print("</statements>\n");
        //'}'
        requireSymbol('}');

        printWriter.print("</whileStatement>\n");
    }

    /**
     * Compiles a return statement
     * ‘return’ expression? ';'
     */
    private void compileReturn(){
        printWriter.print("<returnStatement>\n");

        printWriter.print("<keyword>return</keyword>\n");
        tokenPrintWriter.print("<keyword>return</keyword>\n");

        //Mira si es alguna expresion
        tokenizer.advance();

        if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == ';'){
            printWriter.print("<symbol>;</symbol>\n");
            tokenPrintWriter.print("<symbol>;</symbol>\n");
            printWriter.print("</returnStatement>\n");
            return;
        }

        tokenizer.pointerBack();
        //expression
        compileExpression();
        //';'
        requireSymbol(';');

        printWriter.print("</returnStatement>\n");
    }

    /**
     * Compila si el siguiente es un if
     * 'if' '(' expression ')' '{' statements '}' ('else' '{' statements '}')?
     */
    private void compileIf(){
        printWriter.print("<ifStatement>\n");

        printWriter.print("<keyword>if</keyword>\n");
        tokenPrintWriter.print("<keyword>if</keyword>\n");
        //'('
        requireSymbol('(');
        //expression
        compileExpression();
        //')'
        requireSymbol(')');
        //'{'
        requireSymbol('{');
        //statements
        printWriter.print("<statements>\n");
        compileStatement();
        printWriter.print("</statements>\n");
        //'}'
        requireSymbol('}');

        //mira si es un else
        tokenizer.advance();
        if (tokenizer.tokenType() == JackTokenizer.KEYWORD && tokenizer.keyWord() == JackTokenizer.ELSE){
            printWriter.print("<keyword>else</keyword>\n");
            tokenPrintWriter.print("<keyword>else</keyword>\n");
            //'{'
            requireSymbol('{');
            //statements
            printWriter.print("<statements>\n");
            compileStatement();
            printWriter.print("</statements>\n");
            //'}'
            requireSymbol('}');
        }else {
            tokenizer.pointerBack();
        }

        printWriter.print("</ifStatement>\n");

    }

    private void compileTerm(){

        printWriter.print("<term>\n");

        tokenizer.advance();
        //Mira si es un identifier
        if (tokenizer.tokenType() == JackTokenizer.IDENTIFIER){
            //varName|varName '[' expression ']'|subroutineCall
            String tempId = tokenizer.identifier();

            tokenizer.advance();
            if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == '['){
                printWriter.print("<identifier>" + tempId + "</identifier>\n");
                tokenPrintWriter.print("<identifier>" + tempId + "</identifier>\n");
                //this is an array entry
                printWriter.print("<symbol>[</symbol>\n");
                tokenPrintWriter.print("<symbol>[</symbol>\n");
                //expression
                compileExpression();
                //']'
                requireSymbol(']');
            }else if (tokenizer.tokenType() == JackTokenizer.SYMBOL && (tokenizer.symbol() == '(' || tokenizer.symbol() == '.')){

                tokenizer.pointerBack();tokenizer.pointerBack();
                compileSubroutineCall();
            }else {
                printWriter.print("<identifier>" + tempId + "</identifier>\n");
                tokenPrintWriter.print("<identifier>" + tempId + "</identifier>\n");
                //this is varName
                tokenizer.pointerBack();
            }

        }else{
          //Busca integerConstant o stringConstant o keywordConstant o '(' expression ')'|unaryOp term
            if (tokenizer.tokenType() == JackTokenizer.INT_CONST){
                printWriter.print("<integerConstant>" + tokenizer.intVal() + "</integerConstant>\n");
                tokenPrintWriter.print("<integerConstant>" + tokenizer.intVal() + "</integerConstant>\n");
            }else if (tokenizer.tokenType() == JackTokenizer.STRING_CONST){
                printWriter.print("<stringConstant>" + tokenizer.stringVal() + "</stringConstant>\n");
                tokenPrintWriter.print("<stringConstant>" + tokenizer.stringVal() + "</stringConstant>\n");
            }else if(tokenizer.tokenType() == JackTokenizer.KEYWORD &&
                            (tokenizer.keyWord() == JackTokenizer.TRUE ||
                            tokenizer.keyWord() == JackTokenizer.FALSE ||
                            tokenizer.keyWord() == JackTokenizer.NULL ||
                            tokenizer.keyWord() == JackTokenizer.THIS)){
                    printWriter.print("<keyword>" + tokenizer.getCurrentToken() + "</keyword>\n");
                    tokenPrintWriter.print("<keyword>" + tokenizer.getCurrentToken() + "</keyword>\n");
            }else if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == '('){
                printWriter.print("<symbol>(</symbol>\n");
                tokenPrintWriter.print("<symbol>(</symbol>\n");
                //expression
                compileExpression();
                //')'
                requireSymbol(')');
            }else if (tokenizer.tokenType() == JackTokenizer.SYMBOL && (tokenizer.symbol() == '-' || tokenizer.symbol() == '~')){
                printWriter.print("<symbol>" + tokenizer.symbol() + "</symbol>\n");
                tokenPrintWriter.print("<symbol>" + tokenizer.symbol() + "</symbol>\n");
                //term
                compileTerm();
            }else {
                error("integerConstant|stringConstant|keywordConstant|'(' expression ')'|unaryOp term");
            }
        }

        printWriter.print("</term>\n");
    }

    /**
    * Compila un llamado a una subroutine
    * subroutineName '(' expressionList ')' | (className|varName) '.' subroutineName '(' expressionList ')'
    **/
    private void compileSubroutineCall(){

        tokenizer.advance();
        if (tokenizer.tokenType() != JackTokenizer.IDENTIFIER){
            error("identifier");
        }

        printWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
        tokenPrintWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");

        tokenizer.advance();
        if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == '('){
            //'(' expressionList ')'
            printWriter.print("<symbol>(</symbol>\n");
            tokenPrintWriter.print("<symbol>(</symbol>\n");
            //expressionList
            printWriter.print("<expressionList>\n");
            compileExpressionList();
            printWriter.print("</expressionList>\n");
            //')'
            requireSymbol(')');
        }else if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == '.'){
            //(className|varName) '.' subroutineName '(' expressionList ')'
            printWriter.print("<symbol>.</symbol>\n");
            tokenPrintWriter.print("<symbol>.</symbol>\n");
            //subroutineName
            tokenizer.advance();
            if (tokenizer.tokenType() != JackTokenizer.IDENTIFIER){
                error("identifier");
            }
            printWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
            tokenPrintWriter.print("<identifier>" + tokenizer.identifier() + "</identifier>\n");
            //'('
            requireSymbol('(');
            //Lista de expresiones

            printWriter.print("<expressionList>\n");
            compileExpressionList();
            printWriter.print("</expressionList>\n");
            //')'
            requireSymbol(')');
        }else {
            error("'('|'.'");
        }
    }


    private void compileExpression(){
        printWriter.print("<expression>\n");

        //term
        compileTerm();
        //(op term)*
        do {
            tokenizer.advance();
            //op
            if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.isOp()){
                if (tokenizer.symbol() == '>'){
                    printWriter.print("<symbol>&gt;</symbol>\n");
                    tokenPrintWriter.print("<symbol>&gt;</symbol>\n");
                }else if (tokenizer.symbol() == '<'){
                    printWriter.print("<symbol>&lt;</symbol>\n");
                    tokenPrintWriter.print("<symbol>&lt;</symbol>\n");
                }else if (tokenizer.symbol() == '&') {
                    printWriter.print("<symbol>&amp;</symbol>\n");
                    tokenPrintWriter.print("<symbol>&amp;</symbol>\n");
                }else {
                    printWriter.print("<symbol>" + tokenizer.symbol() + "</symbol>\n");
                    tokenPrintWriter.print("<symbol>" + tokenizer.symbol() + "</symbol>\n");
                }
                //term
                compileTerm();
            }else {
                tokenizer.pointerBack();
                break;
            }

        }while (true);

        printWriter.print("</expression>\n");
    }

    //compila la lista de expresiones separados por ,
    private void compileExpressionList(){
        tokenizer.advance();

        if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == ')'){
            tokenizer.pointerBack();
        }else {

            tokenizer.pointerBack();
            //expression
            compileExpression();
            //(','expression)*
            do {
                tokenizer.advance();
                if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == ','){
                    printWriter.print("<symbol>,</symbol>\n");
                    tokenPrintWriter.print("<symbol>,</symbol>\n");
                    //expression
                    compileExpression();
                }else {
                    tokenizer.pointerBack();
                    break;
                }

            }while (true);

        }
    }

    //lanza una excepción para informar errore
    private void error(String val){
        throw new IllegalStateException("Expected token missing : " + val + " Current token:" + tokenizer.getCurrentToken());
    }

    /**
     * requieren un símbolo cuando sabemos que debe haber tal símbolo
     */
    private void requireSymbol(char symbol){
        tokenizer.advance();
        if (tokenizer.tokenType() == JackTokenizer.SYMBOL && tokenizer.symbol() == symbol){
            printWriter.print("<symbol>" + symbol + "</symbol>\n");
            tokenPrintWriter.print("<symbol>" + symbol + "</symbol>\n");
        }else {
            error("'" + symbol + "'");
        }
    }
}
