"""Helper routines to generate Latex strings for rendering in HTML"""
import sympy 
from sympy import Matrix
import numpy as np
from io import BytesIO
import base64

import matplotlib.pyplot as plt

def getBooleanMatrix(matrix):
    """Generate a boolean matrix for input matrix"""
    mx = np.zeros(matrix.shape, dtype=bool)
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if matrix[i, j] != 0:
                mx[i, j] = True
    return mx

def round_expr(expr, num_digits=4):
    """Method to round the number of digits in sympy output
    Args:
        expr (Expr): Sympy Expression whose digits need to be rounded off
        num_digits (int): precision

    Returns:
        Expr: Sympy expression with rounded digits
    """
    return expr.xreplace(
        {n: round(n, num_digits) for n in expr.atoms(sympy.Number)}
    )

def generateParameterAndStatevalueLatex(composer):
    """Generate a latex table with Parameter names, values and its SI unit
       The latex code is embedded in HTML.
    """
    parameterLatex = """<table id="compositephsparametervalues">
    <tr><th>Parameter</th>
    <th>Value</th>
    <th>SI Units</th>
    </tr>                            
    """
    for k, v in composer.compositeparameters.items():
        parameterLatex += f'<tr><td style="text-align: center; vertical-align: middle;">${sympy.latex(k)}$</td><td style="text-align: center; vertical-align: middle;">${sympy.latex(v["value"])}$</td><td>${sympy.latex(v["units"])}$</td></tr>'
    parameterLatex += "</table>"

    stateValueLatex = """<table id="compositephsstateinitialvalues">
    <tr><th>State Variable</th>
    <th>Initial Value</th>
    <th>SI Units</th>
    </tr>
    """
    for k, v in composer.statevalues.items():
        stateValueLatex += f'<tr><td style="text-align: center; vertical-align: middle;">${sympy.latex(k)}$</td><td style="text-align: center; vertical-align: middle;">${sympy.latex(v["value"])}$</td><td>${sympy.latex(v["units"])}$</td></tr>'
    stateValueLatex += "</table>"

    return f'<table ><tr><td>{parameterLatex}</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td style="vertical-align:top">{stateValueLatex}</td></tr></table>'

def generateLatex(composer):
    """Generate latex code for the composed FTU. The latex code is embedded in HTML."""
    phsequations = r"""
\begin{eqnarray}
\frac{d}{dt}\begin{bmatrix}
    E& 0& 0\\
    0& 0& 0\\
    0& 0& 0
\end{bmatrix}\begin{bmatrix}x\\\hat{u}\\\hat{y}\end{bmatrix}& =& \left [ \begin{bmatrix}
    J& \hat{B}& 0 \\
    -\hat{B}^T& 0& I \\
    0& -I& -\hat{C}
\end{bmatrix}
- 
\begin{bmatrix}
    R& 0& 0 \\
    0& 0& 0 \\
    0& 0& \hat{L}
\end{bmatrix}
\right ]\begin{bmatrix}Qx\\\hat{u}\\\hat{y}\end{bmatrix}
+
\begin{bmatrix}\bar{B}\\0\\0\end{bmatrix}\bar{u}, \\ 
\bar{y} &=& \begin{bmatrix}
    \bar{B}^T & 0& 0
\end{bmatrix} \begin{bmatrix}Qx\\\hat{u}\\\hat{y}\end{bmatrix} .\nonumber
\end{eqnarray}        
    """

    prettyHamiltonian = sympy.latex(round_expr(composer.hamiltonian))
    prettyHamiltonian = prettyHamiltonian.replace("**", "^")
    parameterLatex = generateParameterAndStatevalueLatex(composer)

    latexText = f"""<div><b>Composite Port-Hamiltonian</b> (decimals rounded to 4 digits for presentation)</div><div style="max-height: 500px; max-width: 95%; overflow-y: scroll; overflow-x: scroll;">
            <table style="border-spacing: 30px;">
            <tr>
            <td>
            ${phsequations}$
            </td>
            </tr>
            <tr>
            <td>
                StateVector: $\\boldsymbol{{x}} = {sympy.latex(Matrix(composer.stateVec).T)}^T$
            </td>
            </tr>
            <tr>
            <td>
                $\\mathcal{{H}} = {prettyHamiltonian}$
            </td>
            </tr>
            <tr>           
            <td>
                $            
                \\frac{{\\partial \\mathcal{{H}}(\\boldsymbol{{x}})}}{{\\partial x_i}} = {sympy.latex(round_expr(Matrix(composer.rhsVec).T))}^T$
            </td>
            </tr>
            <tr>
            <td>
                $
                \\boldsymbol{{J}} = {sympy.latex(round_expr(composer.Jcap))}$
            </td>
            </tr>
            <tr>           
            <td>
                $   
                \\boldsymbol{{R}}  = {sympy.latex(round_expr(composer.Rcap))}$
            </td>
            </tr>
            <tr>           
            <td>
                $            
                \\hat{{\\boldsymbol{{B}}}} = {sympy.latex(round_expr(composer.Bcap))}$                    
            </td>
            </tr>
            <tr>           
            <td>
                $            
                \\bar{{\\boldsymbol{{B}}}} = {sympy.latex(round_expr(composer.Bdas.T))}^T$                    
            </td>
            </tr>                
            <tr>
            <td>
                $            
                \\boldsymbol{{E}} = {sympy.latex(round_expr(composer.Ecap))}$                    
            </td>
            </tr>
            <tr>           
            <td>
                $            
                \\boldsymbol{{Q}} = {sympy.latex(round_expr(composer.Qcap))}$
            </td>
            </tr>
            <tr>           
            <td>
                $            
                \\hat{{\\boldsymbol{{C}}}} = {sympy.latex(round_expr(composer.Cmatrix))}$
            </td>
            </tr>
            <tr>           
            <td>
                $            
                \\hat{{\\boldsymbol{{L}}}} = {sympy.latex(round_expr(composer.Lmatrix))}$
            </td>
            </tr>                                
            <tr>           
            <td>
                $
                \\boldsymbol{{u}} = {sympy.latex(composer.uVecSymbols)}$
            </td>
            </tr>
        </table>
        <div style="max-height: 200px; overflow-y: scroll;">
                {parameterLatex}
        </div>            
        </div>
    """
    return latexText

def generateImage(composer):
    """Generate Images for the PHS matrices with black dots for non-zero entries and white dots for zeros
       The latex and images are embedded in HTML.
    """
    # Plot the matrices
    fig, axs = plt.subplots(4, 2, figsize=(10, 10))
    axs[0, 0].imshow(
        getBooleanMatrix(round_expr(composer.Jcap)),
        cmap="Greys",
        interpolation="none",
    )
    axs[0, 0].set_title("$J$", fontweight="bold")
    # Hide X and Y axes label marks
    axs[0, 0].xaxis.set_tick_params(labelbottom=False)
    axs[0, 0].yaxis.set_tick_params(labelleft=False)

    # Hide X and Y axes tick marks
    axs[0, 0].set_xticks([])
    axs[0, 0].set_yticks([])

    axs[0, 1].imshow(
        getBooleanMatrix(round_expr(composer.Rcap)),
        cmap="Greys",
        interpolation="none",
    )
    axs[0, 1].set_title("$R$", fontweight="bold")
    # Hide X and Y axes label marks
    axs[0, 1].xaxis.set_tick_params(labelbottom=False)
    axs[0, 1].yaxis.set_tick_params(labelleft=False)

    # Hide X and Y axes tick marks
    axs[0, 1].set_xticks([])
    axs[0, 1].set_yticks([])

    axs[1, 0].imshow(
        getBooleanMatrix(round_expr(composer.Qcap)),
        cmap="Greys",
        interpolation="none",
    )
    axs[1, 0].set_title("$Q$", fontweight="bold")
    # Hide X and Y axes label marks
    axs[1, 0].xaxis.set_tick_params(labelbottom=False)
    axs[1, 0].yaxis.set_tick_params(labelleft=False)

    # Hide X and Y axes tick marks
    axs[1, 0].set_xticks([])
    axs[1, 0].set_yticks([])

    axs[1, 1].imshow(
        getBooleanMatrix(round_expr(composer.Ecap)),
        cmap="Greys",
        interpolation="none",
    )
    axs[1, 1].set_title("$E$", fontweight="bold")
    # Hide X and Y axes label marks
    axs[1, 1].xaxis.set_tick_params(labelbottom=False)
    axs[1, 1].yaxis.set_tick_params(labelleft=False)

    # Hide X and Y axes tick marks
    axs[1, 1].set_xticks([])
    axs[1, 1].set_yticks([])

    axs[2, 0].imshow(
        getBooleanMatrix(round_expr(composer.Cmatrix)),
        cmap="Greys",
        interpolation="none",
    )
    axs[2, 0].set_title(r"$\hat{C}$", fontweight="bold")
    # Hide X and Y axes label marks
    axs[2, 0].xaxis.set_tick_params(labelbottom=False)
    axs[2, 0].yaxis.set_tick_params(labelleft=False)

    # Hide X and Y axes tick marks
    axs[2, 0].set_xticks([])
    axs[2, 0].set_yticks([])

    axs[2, 1].imshow(
        getBooleanMatrix(round_expr(composer.Lmatrix)),
        cmap="Greys",
        interpolation="none",
    )
    axs[2, 1].set_title(r"$\hat{L}$", fontweight="bold")
    # Hide X and Y axes label marks
    axs[2, 1].xaxis.set_tick_params(labelbottom=False)
    axs[2, 1].yaxis.set_tick_params(labelleft=False)

    # Hide X and Y axes tick marks
    axs[2, 1].set_xticks([])
    axs[2, 1].set_yticks([])

    axs[3, 0].imshow(
        getBooleanMatrix(round_expr(composer.Bcap)),
        cmap="Greys",
        interpolation="none",
    )
    axs[3, 0].set_title(r"$\hat{B}$", fontweight="bold")
    # Hide X and Y axes label marks
    axs[3, 0].xaxis.set_tick_params(labelbottom=False)
    axs[3, 0].yaxis.set_tick_params(labelleft=False)

    # Hide X and Y axes tick marks
    axs[3, 0].set_xticks([])
    axs[3, 0].set_yticks([])

    axs[3, 1].imshow(
        getBooleanMatrix(round_expr(composer.Bdas)),
        cmap="Greys",
        interpolation="none",
    )
    axs[3, 1].set_title("$\\bar{B}$", fontweight="bold")
    # Hide X and Y axes label marks
    axs[3, 1].xaxis.set_tick_params(labelbottom=False)
    axs[3, 1].yaxis.set_tick_params(labelleft=False)

    # Hide X and Y axes tick marks
    axs[3, 1].set_xticks([])
    axs[3, 1].set_yticks([])

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    phsequations = r"""
\begin{eqnarray}
\frac{d}{dt}\begin{bmatrix}
    E& 0& 0\\
    0& 0& 0\\
    0& 0& 0
\end{bmatrix}\begin{bmatrix}x\\\hat{u}\\\hat{y}\end{bmatrix}& =& \left [ \begin{bmatrix}
    J& \hat{B}& 0 \\
    -\hat{B}^T& 0& I \\
    0& -I& -\hat{C}
\end{bmatrix}
- 
\begin{bmatrix}
    R& 0& 0 \\
    0& 0& 0 \\
    0& 0& \hat{L}
\end{bmatrix}
\right ]\begin{bmatrix}Qx\\\hat{u}\\\hat{y}\end{bmatrix}
+
\begin{bmatrix}\bar{B}\\0\\0\end{bmatrix}\bar{u}, \\ 
\bar{y} &=& \begin{bmatrix}
    \bar{B}^T & 0& 0
\end{bmatrix} \begin{bmatrix}Qx\\\hat{u}\\\hat{y}\end{bmatrix} .\nonumber
\end{eqnarray}        
    """

    prettyHamiltonian = sympy.latex(round_expr(composer.hamiltonian))
    prettyHamiltonian = prettyHamiltonian.replace("**", "^")
    parameterLatex = generateParameterAndStatevalueLatex(composer)

    latexText = f"""<div><b>Composite Port-Hamiltonian</b> (decimals rounded to 4 digits for presentation)</div><div style="max-height: 500px; max-width: 95%; overflow-y: scroll; overflow-x: scroll;">
            <table style="border-spacing: 30px;">
            <tr>
            <td>
            ${phsequations}$
            </td>
            </tr>                
            <tr>
            <td colspan="2">
                StateVector: $\\boldsymbol{{x}} = {sympy.latex(Matrix(composer.stateVec).T)}^T$
            </td>
            </tr>
            <tr>
            <td colspan="2">
                $\\mathcal{{H}} = {prettyHamiltonian}$
            </td>
            </tr>
            <tr>           
            <td colspan="2">
                $            
                \\frac{{\\partial \\mathcal{{H}}(\\boldsymbol{{x}})}}{{\\partial x_i}} = {sympy.latex(Matrix(composer.rhsVec).T)}^T$
            </td>
            </tr>
            <tr>           
            <td colspan="2">
                <img src='data:image/png;base64,{data}'/>
            </td>
            </tr>                
            <tr>           
            <td colspan="2">
                $
                \\boldsymbol{{u}} = {sympy.latex(composer.uVecSymbols)}$
            </td>
            </tr>
        </table>
        <div style="max-height: 200px; overflow-y: scroll;">
                {parameterLatex}
        </div>            
        </div>
    """

    return latexText
