from julia import Main

# Inicializa PyJulia
from julia import Julia
Julia(compiled_modules=False)

# Carrega o módulo Julia
Main.include("./microstates.jl")
Microstates = Main.Microstates

from .microstates import MicrostateS, MS2