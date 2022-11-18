 module square(
    // Outputs
    contains_mole, score,
    // Inputs
    hammer, clk_500, current_bonus, bonus_timer
    );

    output reg contains_mole;
    output reg [31:0] score = 0;
    integer score_i = 0;

    input hammer;
    input clk_500;
    input [6:0] elapsed_time;
    input [1:0] current_bonus;
    integer lo;
    integer hi;
    integer num_secs_between_moles = 10;

    reg num_incs_since_mole = 0;

    always @(posedge clk_500) begin
        lo = 250 + (100 - score_i) * 1;
        hi = 250 + (100 - score_i) * 5;
        if (contains_mole) begin
            if (hammer) begin
                if (num_secs_between_
                contains_mole = 0;
            end
            num_incs_since_mole = num_incs_since_mole + 1
            if (num_incs_since_mole > hi) begin
                contains_mole = 0;
            end
            else if (num_incs_since_mole > lo) begin
                if ($random % (hi - lo) == 0) begin
                   contains_mole = 0;
                end
            end
        end
        else begin
            if (hammer) begin
                score_i = score_i - 1;
            end
            if ($random % (500*num_secs_between_moles) == 0) begin
                contains_mole = 1;
            end
        end
        score = score_i;
    end

