export default class Cell {
	private readonly compass:any
	public position:number
	public passages:{[key:string]:boolean}
	public neighbors:{[key:string]:Cell|undefined|null}
	constructor (
		compass:any,
		position:number,
	) {
		// initialize basic information.
		this.compass = compass
		this.position = position

		// initialize passages & neighbors.
		this.passages = {}
		this.neighbors = {}
		for (const direction of this.compass.directions) {
			this.passages[direction] = false
			this.neighbors[direction] = undefined
		}
	}

	public get boundaries (
	):{[key:string]:boolean} {
		// boundaries is the opposite of passages.
		const boundaries:{[key:string]:boolean} = {}
		// loop through passages and reverse values for boundaries.
		for (const direction in this.passages) {
			boundaries[direction] = !this.passages[direction]
		}
		// there you have it!
		return boundaries
	}

	public hasPath (
	):boolean {
		// a direction is either a wall (false) or path (true).
		// check if there's any passages in the values.
		return Object.values(this.passages).includes(true)
		// `.values()` makes a list of booleans from passages.
		// `.includes()` creates a boolean, which is returned.
	}

	public hasWall (
	):boolean {
		// a direction is either a wall (true) or path (false).
		// check if there's any boundaries in the values.
		return Object.values(this.boundaries).includes(true)
		// `.values()` makes a list of booleans from boundaries.
		// `.includes()` creates a boolean, which is returned.
	}

	public hasNeighbor (
		that:Cell,
	):boolean {
		// check if this is a neighbor of that.
		return Object.values(this.neighbors).includes(that)
		// `.values()` makes a list of cells from neighbors.
		// `.includes()` creates a boolean, which is returned.
	}

	public addNeighbor (
		that:Cell,
		direction:string,
	):void {
		// `reversed` is the antipode of a direction.
		// for example, `reversed` of 'north' is 'south'.
		const reversed:string = this.compass.reverse(direction)
		// set neighbors.
		this.neighbors[direction] = that
		that.neighbors[reversed] = this
	}

	public makePathway (
		that:Cell,
		direction:string,
	):void {
		// `reversed` is the antipode of a direction.
		// for example, `reversed` of 'north' is 'south'.
		const reversed:string = this.compass.reverse(direction)
		// set passages.
		this.passages[direction] = true
		that.passages[reversed] = true
	}

}

// valid connected neighbors -> neighbor and true
