'''
# TODO: INSERT DOCSTRING
'''
import sys
import zipfile
import xml.etree.ElementTree as et

# Declare constants for use later on
# Constants should be declared at the module level
# Drogue parachute coefficient of drag (source: FruityChutes)
CD_DROGUE = 1.5
# Main parachute coefficient of drag (source: FruityChutes)
CD_MAIN = 2.2
# Air density at STP in kilograms per cubic meter (source: International Standard Atmosphere)
AIR_DENSITY = 1.22500
# Acceleration due to gravity in meters per second per second (source: SI Standard)
GRAV_ACCEL = 9.80665
# Ratio of a circle's circumference to its diameter
PI = 3.14159

def get_stage_masses(rocket):
    '''
    # TODO: INSERT DOCSTRING
    '''
    # 2D array of time-series masses
    # Each subarray is the mass of a component time
    # Each element is a mass (at a specific time in the simulation)
    masses = []
    # Set which databranch to write to as -1
    # After encountering the first databranch, the code will write to the "0th" array
    databranch = -1
    # For each XML element in the rocket file
    for element in rocket.iter():
        # If the element is a databranch (start of a new set of data)
        if element.tag == 'databranch':
            # Add a new "row" to the 2D array. Each row is a time-series of stage masses
            masses.append([])
            # Increment which branch to write to
            databranch += 1
        # If the element is a data point
        if element.tag == 'datapoint':
            # Pull the mass from the raw data (20th element, delimited by commas)
            mass_string = element.text.split(',')[19]
            # Conver the mass to a double, append it to the current data series
            masses[databranch].append(float(mass_string))
    # The sustainer is the first data series. The final mass is the last data point
    sustainer_mass = masses[0][-1]
    # The booster is the last data series. The final mass is the last data point
    booster_mass = masses[-1][-1]
    # Return a tuple of both masses
    return (sustainer_mass, booster_mass)

def run_calculations(drogue_diameters, main_diameters, stage_mass):
    '''
    # TODO: INSERT DOCSTRING
    '''
    # Print out section mass
    print('Section Mass {0:.2f} (kg)'.format(stage_mass))
    # Print out table top row (TODO: NEEDS FORMATTING)
    print(' Drogue (in.) ', end='')
    print(' Main (in) ', end='')
    print(' V_drogue (ft/s) ', end='')
    print(' V_main (ft/s) ', end='')
    print(' V_both (ft/s) ', end='')
    print(' KE_both (ft-lbf) ', end='')
    print(' Safety Factor')
    # For each possible drogue diameter
    for drogue_diam in drogue_diameters:
        # For each main diameter
        for main_diam in main_diameters:
            # Convert drogue diameter from inches to meters
            drogue_diam_m = drogue_diam * 0.0254
            # Convert main diameter from inches to meters
            main_diam_m = main_diam * 2.54 / 100
            # Calulate and store terminal velocities for each configuration (in meters per second)
            # First element is drogue only, second is main only, third is both deployed
            velocities = terminal_velocity(drogue_diam_m, main_diam_m, stage_mass)
            # Convert velocities from meters per second to feet per second
            velocities_fps = [vel * 3.28084 for vel in velocities]
            # Calculate and store kinetic energies for each configuration (in Joules)
            # First element is drogue only, second is main only, third is both deployed
            kinetic_energies = kinetic_energy(velocities, stage_mass)
            # Convert kinetic energies from Joules to foot-pounds
            kinetic_energies_ft_lbs = [ke * 0.73756 for ke in kinetic_energies]
            # Calculate the safety factor on landing with less than 75 foot-pounds of kinetic energy
            safety_factor = 75 / kinetic_energies_ft_lbs[2]
            # Print out calculated values
            print('      {0}      '.format(drogue_diam), end='')
            print('    {0}    '.format(main_diam), end='')
            print('      {0:.2f}      '.format(velocities_fps[0]), end='')
            print('     {0:.2f}     '.format(velocities_fps[1]), end='')
            print('      {0:.2f}      '.format(velocities_fps[2]), end='')
            print('    {0:06.2f}    '.format(kinetic_energies_ft_lbs[2]), end='')
            print('       {0:.2f}       '.format(safety_factor))
    # Print out a new line after all stage calculations
    print()

def terminal_velocity(drogue_diam, main_diam, stage_mass):
    '''
    # TODO: INSERT DOCSTRING
    '''
    # Calculate area of drogue parachute
    drogue_area = PI * ((drogue_diam / 2) ** 2)
    # Calculate area of main parachute
    main_area = PI * ((main_diam / 2) ** 2)
    # Calculate weight force of stage
    weight_force = stage_mass * GRAV_ACCEL
    # Calculate the drag factor of drogue parachute
    drogue_drag = 0.5 * AIR_DENSITY * CD_DROGUE * drogue_area
    # Calculate the drag factor of the main parachute
    main_drag = 0.5 * AIR_DENSITY * CD_MAIN * main_area
    # Calculate the terminal velocity of the stage with just the drogue parachute
    v_drogue = (weight_force / drogue_drag) ** 0.5
    # Calculate the terminal velocity of the stage with just the main parachute
    v_main = (weight_force / main_drag) ** 0.5
    # Calculate the terminal velocity of the stage with both parachutes deployed
    v_both = (weight_force / (drogue_drag + main_drag)) ** 0.5
    # Return an array with all three calculated velocities
    return [v_drogue, v_main, v_both]

def kinetic_energy(velocities, stage_mass):
    '''
    # TODO: INSERT DOCSTRING
    '''
    # Calculate kinetic energy of the stage with just the drogue parachute
    ke_drogue = 0.5 * stage_mass * (velocities[0] ** 2)
    # Calculate kinetic energy of the stage with just the main parachute
    ke_main = 0.5 * stage_mass * (velocities[1] ** 2)
    # Calculate kinetic energy of the stage with both parachutes deployed
    ke_both = 0.5 * stage_mass * (velocities[2] ** 2)
    # Return an array with all three calculated kinetic energies
    return [ke_drogue, ke_main, ke_both]

def main():
    '''
    #TODO: INSERT DOCSTRING
    '''
    # Take the second system argument and create a zipfile from it
    rocket_zip = zipfile.ZipFile(sys.argv[1], 'r')
    # Parse the zip file into an XML ElementTree object
    rocket = et.fromstring(rocket_zip.read('rocket.ork'))
    # Calculate the sustainer and booster section masses
    sustainer_mass, booster_mass = get_stage_masses(rocket)
    # Drogue parachute diameters to test (NOTE: IN INCHES)
    drogue_diameters = [24, 30, 36] # TODO: ALLOW USER INPUT
    # Main parachute diameters to test (NOTE: IN INCHES)
    main_diameters = [108, 120, 132, 144, 156, 168, 180] # TODO: ALLOW USER INPUT
    # Run parachute calculations for booster section
    run_calculations(drogue_diameters, main_diameters, booster_mass)
    # Run parachute calculations for sustainer section
    run_calculations(drogue_diameters, main_diameters, sustainer_mass)

# I'm not sure what this code does I copied it
if __name__ == '__main__':
    # Run the main method I guess ¯\_(ツ)_/¯
    main()
