from julia import Main
import julia

julia.install()

# Carrega o módulo Julia
Main.include("./microstates.jl")
Microstates = Main.Microstates

def MicrostateS(Serie, Threshold, Window_Size=None, StatsBlock=2, RP_percent=0.05):
    '''
    Function to calculate the entropy and the microstates probability
    ------------------------------------------------------------------
    Serie       : Time Series to be evaluated (can be multi-dimensional)
    Threshold   : Recurrence threshold (epsilon)
    Window_Size : Number of points in data to be evaluated (if not declared it will be initialized as len(Serie)
    StatsBlock  : Size of the MicroState, matrix with size StatsBlock x StatsBlock
    RP_percent  : Percent of samples in RP to be randomly selected
    '''
     
    if Window_Size is None:
        Window_Size = len(Serie)
    return Microstates.MicrostateS(Serie, Threshold, Window_Size, StatsBlock, RP_percent)

def MS2(Serie, Threshold, Window_Size=None, StatsBlock=2, RP_percent=0.05):
    '''
    Function to calculate the entropy and the microstates probability
    ------------------------------------------------------------------
    Serie       : Time Series to be evaluated (can be multi-dimensional)
    Threshold   : Recurrence threshold (epsilon)
    Window_Size : Number of points in data to be evaluated (if not declared it will be initialized as len(Serie)
    StatsBlock  : Size of the MicroState, matrix with size StatsBlock x StatsBlock
    RP_percent  : Percent of samples in RP to be randomly selected
    '''
    if Window_Size is None:
        Window_Size = len(Serie)
    return Microstates.MS2(Serie, Threshold, Window_Size, StatsBlock, RP_percent)
