module Microstates

export MicrostateS, MS2

using Random, LinearAlgebra

export MicrostateS, MS2

function MicrostateS(Serie, Threshold, Window_Size=nothing, StatsBlock=2, RP_percent=0.05)
    if Window_Size === nothing
        Window_Size = length(Serie)
    end
    
    Max_Micro = 2 ^ (StatsBlock * StatsBlock)
    Sample_N = Int(floor(RP_percent * Window_Size * Window_Size))
    
    MicroStates = zeros(Max_Micro)
    Stats = zeros(Max_Micro)
    
    x_rand = rand(1:(Window_Size - StatsBlock), Sample_N)
    y_rand = rand(1:(Window_Size - StatsBlock), Sample_N)
    
    pow_vec = 2 .^ (0:(StatsBlock * StatsBlock - 1)) |> reshape(StatsBlock, StatsBlock)
    
    for count in 1:Sample_N
        Add = 0
        x_base = x_rand[count]
        y_base = y_rand[count]
        
        x_block = Serie[x_base:x_base + StatsBlock - 1]
        y_block = Serie[y_base:y_base + StatsBlock - 1]
        
        binary_matrix = (abs.(x_block .- y_block') .<= Threshold) |> Int
        
        Add = sum(binary_matrix .* pow_vec)
        Stats[Add + 1] += 1
    end
    
    MicroStates .= Stats ./ Sample_N
    
    nonzero_probs = MicroStates[MicroStates .> 0]
    S = -sum(nonzero_probs .* log.(nonzero_probs))
    
    return MicroStates, S
end

function MS2(Serie, Threshold, Window_Size=nothing, StatsBlock=2, RP_percent=0.05)
    if Window_Size === nothing
        Window_Size = length(Serie)
    end
    
    Max_Micro = 2 ^ (StatsBlock * StatsBlock)
    Sample_N = Int(floor(RP_percent * Window_Size * Window_Size))
    
    MicroStates = zeros(Max_Micro)
    Stats = zeros(Max_Micro)
    
    x_rand = rand(1:(Window_Size - StatsBlock), Sample_N)
    y_rand = rand(1:(Window_Size - StatsBlock), Sample_N)
    
    pow_vec = 2 .^ (0:(StatsBlock * StatsBlock - 1))
    
    for count in 1:Sample_N
        Add = 0
        for count_x in 1:StatsBlock
            for count_y in 1:StatsBlock
                if abs(Serie[x_rand[count] + count_x - 1] - Serie[y_rand[count] + count_y - 1]) <= Threshold
                    a_binary = 1
                else
                    a_binary = 0
                end
                Add += a_binary * pow_vec[count_y + (count_x - 1) * StatsBlock - 1]
            end
        end
        Stats[Add + 1] += 1
    end
    
    S = 0.0
    
    MicroStates .= Stats ./ Sample_N
    
    for k in 1:Max_Micro
        if Stats[k] > 0
            S += -MicroStates[k] * log(MicroStates[k])
        end
    end
    
    return MicroStates, S
end

end
