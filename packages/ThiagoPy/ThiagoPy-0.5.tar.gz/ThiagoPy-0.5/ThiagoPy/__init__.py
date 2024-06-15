from julia import Main
import os

# Inicializa PyJulia
from julia import Julia
Julia(compiled_modules=False)

current_dir = os.path.dirname(os.path.abspath(__file__))
julia_file = os.path.join(current_dir, 'microstates.jl')
Main.include(julia_file)
Microstates = Main.Microstates

from .microstates import MicrostateS, MS2