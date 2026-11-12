library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tt_um_new_chip is
    port (
        ui_in   : in  std_logic_vector(7 downto 0);  -- 8 bit IN
        uo_out  : out std_logic_vector(7 downto 0);  -- 8 bit OUT

        uio_in  : in  std_logic_vector(7 downto 0);  -- 8 bit IN from R/W
        uio_out : out std_logic_vector(7 downto 0);  -- 8 bit OUT from R/W
        uio_oe  : out std_logic_vector(7 downto 0);  -- mode for R/W pin by pin  ('1' is out)  (can technically be changed mid run)

        ena     : in  std_logic;                     -- don't care (is actually a "turned on signal" but it doesn't matter)
        clk     : in  std_logic;                     
        rst_n   : in  std_logic
    );
end tt_um_new_chip;




architecture Behavioral of tt_um_new_chip is
begin

    --uo_out <= std_logic_vector( resize( unsigned(ui_in) * unsigned(uio_in), 8 ));

    uo_out <= std_logic_vector( resize( to_unsigned(256, 9) / resize(unsigned(ui_in), 9), 8 ));

    uio_out <= "00000000";
    uio_oe <= "00000000";

end Behavioral;