import streamlit as st

from civilpy.transportation.rail_network_simulator.rail_simulator import *

# Create the World Object
W = World(
    name="AF-RO",
    deltan=1,
    tmax=1000,
    print_mode=1, save_mode=0, show_mode=1,
    random_seed=0
)

# Define Southern (Low MP) Orgins
W.addNode("yard1_org", 0, 14)      # 0
W.addNode("y1e", 3, 14)            # 1
W.addNode("yard2_org", 0, 12)      # 2
W.addNode("yard3_org", 0, 10)      # 3
W.addNode("main3_org", 0, 8)       # 4
W.addNode("main2_org", 0, 6)       # 5
W.addNode("main1_org", 0, 4)       # 6
W.addNode("NS_org", 14, 2)         # 7
W.addNode("NS_yard", 0, 2)         # 8
W.addNode("Setoff Track", 22, 2)   # 9
W.addNode("Setoff End", 26, 2)     # 10

# Define Switches
W.addNode("0_S", 5, 12)            # 11
W.addNode("1_S", 3, 12)            # 12
W.addNode("3_S", 5, 10)            # 13
W.addNode("5_S", 7, 10)            # 14
W.addNode("7_S", 9, 8)             # 15
W.addNode("9_S", 9, 6)             # 16
W.addNode("11_S", 11, 4)           # 17
W.addNode("13_S", 11, 8)           # 18
W.addNode("19_S", 13, 6)           # 19
W.addNode("21_S", 15, 6)           # 20
W.addNode("23_S", 17, 8)           # 21
W.addNode("25_S", 16, 6)           # 22
W.addNode("27_S", 16, 4)           # 23
W.addNode("29_S", 18, 4)           # 24
W.addNode("31_S", 19, 4)           # 25
W.addNode("33_S", 21, 6)           # 26
W.addNode("35_S", 20, 4)           # 27
W.addNode("37_S", 22, 6)           # 28
W.addNode("39_S", 24, 4)           # 29
W.addNode("41_S", 20, 8)           # 30
W.addNode("43_S", 22, 10)          # 31
W.addNode("45_S", 23, 6)           # 32
W.addNode("47_S", 25, 8)           # 33

# Add Destinations
W.addNode("main0_dest", 30, 4)     # 34
W.addNode("main1_dest", 30, 6)     # 35
W.addNode("main2_dest", 30, 8)     # 36
W.addNode("main3_dest", 30, 10)    # 37

# Define links between Values
# Crossovers
W.addLink("1-3X", "1_S", "3_S", length=50, free_flow_speed=30, number_of_lanes=1)      # 0
W.addLink("5-7X", "5_S", "7_S", length=50, free_flow_speed=30, number_of_lanes=1)      # 1
W.addLink("9-11X", "9_S", "11_S", length=50, free_flow_speed=30, number_of_lanes=1)    # 2
W.addLink("13-19X", "13_S", "19_S", length=50, free_flow_speed=30, number_of_lanes=1)  # 3
W.addLink("21-23X", "21_S", "23_S", length=50, free_flow_speed=30, number_of_lanes=1)  # 4
W.addLink("25-29X", "25_S", "29_S", length=50, free_flow_speed=30, number_of_lanes=1)  # 5
W.addLink("31-33X", "31_S", "33_S", length=50, free_flow_speed=30, number_of_lanes=1)  # 6
W.addLink("37-39X", "37_S", "39_S", length=50, free_flow_speed=30, number_of_lanes=1)  # 7
W.addLink("41-43X", "41_S", "43_S", length=50, free_flow_speed=30, number_of_lanes=1)  # 8
W.addLink("45-47X", "45_S", "47_S", length=50, free_flow_speed=30, number_of_lanes=1)  # 9

# Yard Segments
W.addLink("yard1", "yard1_org", "y1e", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)                  # 10
W.addLink("y1_2", "y1e", "0_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)                         # 11
W.addLink("yard2", "yard2_org", "1_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)                  # 12
W.addLink("NS", "NS_org", "27_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)                       # 13
W.addLink("NS Yard", "NS_yard", "NS_org", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)               # 14
W.addLink("yard0_0", "1_S", "0_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)                      # 15
W.addLink("Setoff_Track", "Setoff Track", "Setoff End", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1) # 16
W.addLink("Setoff Track", "35_S", "Setoff Track", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)       # 17

# Main 0 Segments
W.addLink("0_0", "main1_org", "11_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)  # 18
W.addLink("0_1", "11_S", "27_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)       # 19
W.addLink("0_2", "27_S", "29_S", length=50, free_flow_speed=50, number_of_lanes=1)                           # 20
W.addLink("0_3", "29_S", "31_S", length=50, free_flow_speed=50, number_of_lanes=1)                           # 21
W.addLink("0_4", "31_S", "35_S", length=50, free_flow_speed=50, number_of_lanes=1)                           # 22
W.addLink("0_5", "35_S", "39_S", length=50, free_flow_speed=50, number_of_lanes=1)                           # 23
W.addLink("0_6", "39_S", "main0_dest", length=50, free_flow_speed=50, number_of_lanes=1)                     # 24

# Main 1 Segments
W.addLink("1_0", "main2_org", "9_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)    # 25
W.addLink("1_1", "9_S", "19_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)         # 26
W.addLink("1_2", "19_S", "21_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)        # 27
W.addLink("1_3", "21_S", "25_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)        # 28
W.addLink("1_4", "25_S", "33_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)        # 29
W.addLink("1_5", "33_S", "37_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)        # 30
W.addLink("1_6", "37_S", "45_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)        # 31
W.addLink("1_7", "45_S", "main1_dest", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)  # 32

# Main 2 Segments
W.addLink("2_0", "main3_org", "7_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)    # 33
W.addLink("2_1", "7_S", "13_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)         # 34
W.addLink("2_2", "13_S", "23_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)        # 35
W.addLink("2_3", "23_S", "41_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)        # 36
W.addLink("2_4", "41_S", "47_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)        # 37
W.addLink("2_5", "47_S", "main2_dest", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)  # 38

# Main 3 Segments
W.addLink("3_0", "yard3_org", "3_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)    # 39
W.addLink("3_1", "3_S", "5_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)          # 40
W.addLink("3_2", "5_S", "43_S", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)         # 41
W.addLink("3_3", "43_S", "main3_dest", length=50, free_flow_speed=50, number_of_lanes=1, merge_priority=0.1)  # 42

# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center; color: teal;'>Rail Network Simulator</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: green;'>Outage Selection</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    col1.header('Before AF')
    option1 = st.checkbox("Yard 1 Outage", key='pre_AF_yard1_disabled')
    option2 = st.checkbox("Yard 2 Outage", key='pre_AF_yard2_disabled')
    option3 = st.checkbox("Yard 3 Outage", key='pre_AF_yard3_disabled')
    option4 = st.checkbox("Main 3 Outage", key='pre_AF_main3_disabled')
    option5 = st.checkbox("Main 2 Outage", key='pre_AF_main2_disabled')
    option6 = st.checkbox("Main 1 Outage", key='pre_AF_main1_disabled')
    option7 = st.checkbox("NS Outage",     key='pre_AF_ns_disabled')

with col2:
    col2.header('AF-Slaters Lane')
    AFSlatersMain3Closed = st.checkbox("Main 3 Outage", key='AF_Slaters_main3_disabled')
    AFSlatersMain2Closed = st.checkbox("Main 2 Outage", key='AF_Slaters_main2_disabled')
    AFSlatersMain1Closed = st.checkbox("Main 1 Outage", key='AF_Slaters_main1_disabled')
    AFSlatersMain0Closed = st.checkbox("Main 0 Outage", key='AF_Slaters_main0_disabled')

with col3:
    col3.header('Slaters Lane-RO')
    option12 = st.checkbox("Main 3 Outage", key='Slaters_RO_main3_disabled')
    option13 = st.checkbox("Main 2 Outage", key='Slaters_RO_main2_disabled')
    option14 = st.checkbox("Main 1 Outage", key='Slaters_RO_main1_disabled')
    option15 = st.checkbox("Main 0 Outage", key='Slaters_RO_main0_disabled')

with col4:
    col4.header('After RO')
    option16 = st.checkbox("Main 3 Outage", key='After_RO_main3_disabled')
    option17 = st.checkbox("Main 2 Outage", key='After_RO_main2_disabled')


# Update the graph depending on what routes are closed
# 1 combination with all 4 tracks closed
if AFSlatersMain0Closed and AFSlatersMain1Closed and AFSlatersMain2Closed and AFSlatersMain3Closed:
    for link in W.LINKS:
        link.color = 'red'
    for node in W.NODES:
        node.color = 'red'

# 4 combos of 3 tracks closed
elif AFSlatersMain0Closed and AFSlatersMain1Closed and AFSlatersMain2Closed:
    # Example of closing main 0/1/2
    W.LINKS[1].color = 'red'  # 5-7X
    W.LINKS[2].color = 'red'  # 9-11X
    W.LINKS[3].color = 'red'  # 13-19X
    W.LINKS[5].color = 'red'  # 25-29X
    W.LINKS[6].color = 'red'  # 31-33X
    W.LINKS[7].color = 'red'  # 37-39X
    W.LINKS[9].color = 'red'  # 45-47X
    W.LINKS[13].color = 'red'  # NS
    W.LINKS[14].color = 'red'  # NS Yard
    W.LINKS[18].color = 'red'  # 0_0
    W.LINKS[19].color = 'red'  # 0_1
    W.LINKS[20].color = 'red'  # 0_2
    W.LINKS[21].color = 'red'  # 0_3
    W.LINKS[22].color = 'red'  # 0_4
    W.LINKS[23].color = 'red'  # 0_5
    W.LINKS[24].color = 'red'  # 0_6
    W.LINKS[29].color = 'red'  # 1_4
    W.LINKS[30].color = 'red'  # 1_5
    W.LINKS[31].color = 'red'  # 1_6
    W.LINKS[32].color = 'red'  # 1_7
    W.LINKS[37].color = 'red'  # 2_5
    W.LINKS[38].color = 'red'  # 2_6

    W.NODES[6].color = 'red'  # main1_org
    W.NODES[7].color = 'red'  # NS_org
    W.NODES[8].color = 'red'  # NS_Yard
    W.NODES[14].color = 'red'  # 5_S
    W.NODES[15].color = 'red'  # 7_S
    W.NODES[16].color = 'red'  # 9_S
    W.NODES[17].color = 'red'  # 11_S
    W.NODES[18].color = 'red'  # 13_S
    W.NODES[19].color = 'red'  # 19_S
    W.NODES[23].color = 'red'  # 27_S
    W.NODES[25].color = 'red'  # 31_S
    W.NODES[26].color = 'red'  # 28_S
    W.NODES[27].color = 'red'  # 35_S
    W.NODES[22].color = 'red'  # 25_S
    W.NODES[24].color = 'red'  # 29_S
    W.NODES[28].color = 'red'  # 37_S
    W.NODES[29].color = 'red'  # 39_S
    W.NODES[32].color = 'red'  # 45_S
    W.NODES[33].color = 'red'  # 47_S
    W.NODES[34].color = 'red'  # main0_dest
    W.NODES[35].color = 'red'  # Main1_dest
    W.NODES[36].color = 'red'  # main2_dest

elif AFSlatersMain0Closed and AFSlatersMain1Closed and AFSlatersMain3Closed:
    # Example of closing main 0/1/3
    W.LINKS[7].color = 'red'  # 37-39X
    W.LINKS[8].color = 'red'  # 41-43X
    W.LINKS[23].color = 'red'  # 0_5
    W.LINKS[24].color = 'red'  # 0_6
    W.LINKS[32].color = 'red'  # 1_7
    W.LINKS[42].color = 'red'  # 3_3

    W.NODES[28].color = 'red'  # 37_S
    W.NODES[29].color = 'red'  # 39_S
    W.NODES[30].color = 'red'  # 41_S
    W.NODES[31].color = 'red'  # 43_S
    W.NODES[34].color = 'red'  # main0_dest
    W.NODES[35].color = 'red'  # Main1_dest
    W.NODES[37].color = 'red'  # main3_dest

elif AFSlatersMain0Closed and AFSlatersMain2Closed and AFSlatersMain3Closed:
    # Example of closing main 0/2/3
    W.LINKS[4].color = 'red'  # 21-23X
    W.LINKS[7].color = 'red'  # 37-39X
    W.LINKS[8].color = 'red'  # 41-43X
    W.LINKS[9].color = 'red'  # 45-47X
    W.LINKS[23].color = 'red'  # 0_5
    W.LINKS[24].color = 'red'  # 0_6
    W.LINKS[35].color = 'red'  # 2_2
    W.LINKS[35].color = 'red'  # 2_3
    W.LINKS[36].color = 'red'  # 2_4
    W.LINKS[37].color = 'red'  # 2_5
    W.LINKS[38].color = 'red'  # 2_6
    W.LINKS[41].color = 'red'  # 3_2
    W.LINKS[42].color = 'red'  # 3_3

    W.NODES[18].color = 'red'  # 17_S
    W.NODES[20].color = 'red'  # 21_S
    W.NODES[21].color = 'red'  # 23_S
    W.NODES[28].color = 'red'  # 37_S
    W.NODES[29].color = 'red'  # 39_S
    W.NODES[30].color = 'red'  # 41_S
    W.NODES[31].color = 'red'  # 43_S
    W.NODES[32].color = 'red'  # 45_S
    W.NODES[33].color = 'red'  # 47_S
    W.NODES[34].color = 'red'  # main0_dest
    W.NODES[36].color = 'red'  # main2_dest
    W.NODES[37].color = 'red'  # main3_dest

elif AFSlatersMain1Closed and AFSlatersMain2Closed and AFSlatersMain3Closed:
    # Example of closing main 1/2/3
    W.LINKS[4].color = 'red'  # 21-23X
    W.LINKS[6].color = 'red'  # 31-33X
    W.LINKS[7].color = 'red'  # 37-39X
    W.LINKS[8].color = 'red'  # 41-43X
    W.LINKS[9].color = 'red'  # 45-47X
    W.LINKS[29].color = 'red'  # 1_4
    W.LINKS[30].color = 'red'  # 1_5
    W.LINKS[31].color = 'red'  # 1_6
    W.LINKS[32].color = 'red'  # 1_7
    W.LINKS[35].color = 'red'  # 2_2
    W.LINKS[36].color = 'red'  # 2_4
    W.LINKS[37].color = 'red'  # 2_5
    W.LINKS[38].color = 'red'  # 2_6
    W.LINKS[41].color = 'red'  # 3_2
    W.LINKS[42].color = 'red'  # 3_3

    W.NODES[18].color = 'red'  # 13_S
    W.NODES[20].color = 'red'  # 21_S
    W.NODES[21].color = 'red'  # 23_S
    W.NODES[25].color = 'red'  # 31_S
    W.NODES[26].color = 'red'  # 33_S
    W.NODES[28].color = 'red'  # 37_S
    W.NODES[29].color = 'red'  # 39_S
    W.NODES[30].color = 'red'  # 41_S
    W.NODES[31].color = 'red'  # 43_S
    W.NODES[32].color = 'red'  # 45_S
    W.NODES[33].color = 'red'  # 47_S
    W.NODES[35].color = 'red'  # Main1_dest
    W.NODES[36].color = 'red'  # main2_dest
    W.NODES[37].color = 'red'  # main3_dest

# 6 combos of 2 tracks closed
elif AFSlatersMain0Closed and AFSlatersMain1Closed:
    # Example of closing main 0/1
    W.LINKS[7].color = 'red'  # 37-39X
    W.LINKS[23].color = 'red'  # 0_5
    W.LINKS[24].color = 'red'  # 0_6
    W.LINKS[32].color = 'red'  # 1_7

    W.NODES[28].color = 'red'  # 37_S
    W.NODES[29].color = 'red'  # 39_S
    W.NODES[34].color = 'red'  # main0_dest
    W.NODES[35].color = 'red'  # Main1_dest

elif AFSlatersMain0Closed and AFSlatersMain2Closed:
    # Example of closing main 0/2
    W.LINKS[7].color = 'red'  # 37-39X
    W.LINKS[9].color = 'red'  # 45-47X
    W.LINKS[23].color = 'red'  # 0_5
    W.LINKS[24].color = 'red'  # 0_6
    W.LINKS[37].color = 'red'  # 2_5
    W.LINKS[38].color = 'red'  # 2_6

    W.NODES[28].color = 'red'  # 37_S
    W.NODES[29].color = 'red'  # 39_S
    W.NODES[32].color = 'red'  # 45_S
    W.NODES[33].color = 'red'  # 47_S
    W.NODES[34].color = 'red'  # main0_dest
    W.NODES[36].color = 'red'  # main2_dest

elif AFSlatersMain0Closed and AFSlatersMain3Closed:
    # Example of closing main 0/3
    W.LINKS[7].color = 'red'  # 37-39X
    W.LINKS[8].color = 'red'  # 41-43X
    W.LINKS[23].color = 'red'  # 0_5
    W.LINKS[24].color = 'red'  # 0_6
    W.LINKS[42].color = 'red'  # 3_3

    W.NODES[28].color = 'red'  # 37_S
    W.NODES[29].color = 'red'  # 39_S
    W.NODES[30].color = 'red'  # 41_S
    W.NODES[31].color = 'red'  # 43_S
    W.NODES[34].color = 'red'  # main0_dest
    W.NODES[37].color = 'red'  # main3_dest

elif AFSlatersMain1Closed and AFSlatersMain2Closed:
    # Example of closing main 1/2
    W.LINKS[6].color = 'red'  # 31-33X
    W.LINKS[9].color = 'red'  # 45-47X
    W.LINKS[31].color = 'red'  # 1_6
    W.LINKS[32].color = 'red'  # 1_7
    W.LINKS[37].color = 'red'  # 2_5
    W.LINKS[38].color = 'red'  # 2_6

    W.NODES[25].color = 'red'  # 31_S
    W.NODES[26].color = 'red'  # 33_S
    W.NODES[32].color = 'red'  # 45_S
    W.NODES[33].color = 'red'  # 47_S
    W.NODES[35].color = 'red'  # Main1_dest
    W.NODES[36].color = 'red'  # main2_dest

elif AFSlatersMain2Closed and AFSlatersMain3Closed:
    # Example of closing main 2/3
    W.LINKS[4].color = 'red'  # 21-23X
    W.LINKS[8].color = 'red'  # 41-43X
    W.LINKS[9].color = 'red'  # 45-47X
    W.LINKS[35].color = 'red'  # 2_2
    W.LINKS[36].color = 'red'  # 2_4
    W.LINKS[37].color = 'red'  # 2_5
    W.LINKS[38].color = 'red'  # 2_6
    W.LINKS[41].color = 'red'  # 3_2
    W.LINKS[42].color = 'red'  # 3_3

    W.NODES[18].color = 'red'  # 13_S
    W.NODES[20].color = 'red'  # 21_S
    W.NODES[21].color = 'red'  # 23_S
    W.NODES[30].color = 'red'  # 41_S
    W.NODES[31].color = 'red'  # 43_S
    W.NODES[32].color = 'red'  # 45_S
    W.NODES[33].color = 'red'  # 47_S
    W.NODES[36].color = 'red'  # main2_dest
    W.NODES[37].color = 'red'  # main3_dest

elif AFSlatersMain1Closed and AFSlatersMain3Closed:
    # Example of closing main 1/3
    W.LINKS[8].color = 'red'  # 41-43X
    W.LINKS[32].color = 'red'  # 1_7
    W.LINKS[42].color = 'red'  # 3_3

    W.NODES[30].color = 'red'  # 41_S
    W.NODES[31].color = 'red'  # 43_S
    W.NODES[35].color = 'red'  # Main1_dest
    W.NODES[37].color = 'red'  # main3_dest

elif AFSlatersMain3Closed and AFSlatersMain2Closed:
    W.LINKS[42].color = 'red'
    W.LINKS[41].color = 'red'
    W.LINKS[8].color = 'red'
    W.LINKS[4].color = 'red'
    W.LINKS[36].color = 'red'
    W.LINKS[37].color = 'red'
    W.LINKS[38].color = 'red'
    W.LINKS[9].color = 'red'
    W.LINKS[35].color = 'red'

    W.NODES[20].color = 'red'
    W.NODES[21].color = 'red'
    W.NODES[30].color = 'red'
    W.NODES[31].color = 'red'
    W.NODES[37].color = 'red'
    W.NODES[32].color = 'red'
    W.NODES[33].color = 'red'
    W.NODES[36].color = 'red'

# 4 versions of 1 track closed (0,0,0,0 is 16th possible combo and not included since it's the default state)
elif AFSlatersMain3Closed:
    W.LINKS[8].color = 'red'
    W.LINKS[41].color = 'red'
    W.LINKS[42].color = 'red'

    W.NODES[30].color = 'red'
    W.NODES[31].color = 'red'
    W.NODES[37].color = 'red'

elif AFSlatersMain2Closed:
    W.LINKS[37].color = 'red'
    W.LINKS[38].color = 'red'
    W.LINKS[9].color = 'red'

    W.NODES[30].color = 'red'
    W.NODES[32].color = 'red'
    W.NODES[33].color = 'red'
    W.NODES[36].color = 'red'

elif AFSlatersMain1Closed:
    W.LINKS[32].color = 'red'

    W.NODES[35].color = 'red'
    W.NODES[32].color = 'red'

elif AFSlatersMain0Closed:
    W.LINKS[7].color = 'red'
    W.LINKS[24].color = 'red'
    W.LINKS[23].color = 'red'

    W.NODES[28].color = 'red'
    W.NODES[29].color = 'red'
    W.NODES[34].color = 'red'


def run_analysis():
    W.exec_simulation()
    W.analyzer.print_simple_stats()

    W.analyzer.network_anim(animation_speed_inverse=15, timestep_skip=30, detailed=0, figsize=(6, 6))
    # gif from local file
    file_ = open("D:\\Jetbrains\\PycharmProjects\\civilpy\\src\\civilpy\\transportation\\rail_network_simulator\\outAF-RO\\anim_network0.gif", "rb")
    contents = file_.read()


with st.spinner('Running Analysis...'):
    st.button(label="Run Analysis", on_click=run_analysis())


st.pyplot(W.show_network(figsize=(20, 20)))



