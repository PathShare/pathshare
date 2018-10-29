import { Component, OnInit } from '@angular/core';
import { Ride } from '../shared/model/ride';
import { SearchService } from './search.service';

@Component({
  selector: 'app-trip-search',
  templateUrl: './trip-search.component.html',
  styleUrls: ['./trip-search.component.css']
})
export class TripSearchComponent implements OnInit {

  allTrips: Ride[];

  constructor(private searchService: SearchService) { }

  ngOnInit() {
    this.searchService.getAllRides().subscribe(rides => {
      rides.forEach(ride => {
        console.log(ride.departureLocation);
      });
    });
  }

}
