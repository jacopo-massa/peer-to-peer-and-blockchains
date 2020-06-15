/*
 * Copyright 2010 Aalto University, ComNet
 * Released under GPLv3. See LICENSE.txt for details.
 */
package movement;

import core.Coord;
import core.Settings;
import core.SettingsError;

import java.lang.reflect.Array;
import java.util.ArrayList;

/**
 * Random hotspot movement model. Creates zig-zag paths within the
 * simulation area, among random-generated hotsposts.
 */
public class RandomHotspot extends MovementModel {

	/** how many waypoints should there be per path */
	private static final int PATH_LENGTH = 1;
	/** Hotspost namespace */
	private static final String HS_NS = "Hotspot";
	private Coord lastWaypoint;
	public static ArrayList<Coord> hotspots;

	public RandomHotspot(Settings settings) {
		super(settings);
		generateHotspots();
	}

	protected RandomHotspot(RandomHotspot rwp) {
		super(rwp);
		hotspots = rwp.hotspots;
	}

	/**
	 * Returns a possible (random) placement for a host
	 * @return Random position on the map
	 */
	@Override
	public Coord getInitialLocation() {
		assert rng != null : "MovementModel not initialized!";
		Coord c = randomCoord();

		this.lastWaypoint = c;
		return c;
	}

	@Override
	public Path getPath() {
		Path p;
		p = new Path(generateSpeed());
		p.addWaypoint(lastWaypoint.clone());
		Coord c = lastWaypoint;

		for (int i=0; i<PATH_LENGTH; i++) {
			c = randomHotspot();
			p.addWaypoint(c);
		}

		this.lastWaypoint = c;
		return p;
	}

	@Override
	public RandomHotspot replicate() {
		return new RandomHotspot(this);
	}

	protected Coord randomCoord() {
		return new Coord(rng.nextDouble() * getMaxX(),
				rng.nextDouble() * getMaxY());
	}

	private void generateHotspots() {
		Settings settings = new Settings(HS_NS);
		hotspots = new ArrayList<>();
		try {
			int numberOfHotspots = settings.getInt("nrofHS");
			if (numberOfHotspots < 0)
				throw new SettingsError("");

			for(int i=0; i<numberOfHotspots; i++)
				hotspots.add(randomCoord());

		} catch (SettingsError se) {
			System.err.println("Can't find '" + HS_NS + "nrofHS', or it has a value < 1");
			System.err.println("Caught at " + se.getStackTrace()[0]);
			System.exit(-1);
		}
	}

	private Coord randomHotspot() {
		return hotspots.get(rng.nextInt(hotspots.size()));
	}
}
