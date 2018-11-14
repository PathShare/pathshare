import { Component, OnInit } from '@angular/core';
import { SearchFormService } from '../shared/services/search-form.service';
import { SearchService } from '../trip-search/search.service';
import { Ride } from '../shared/model/ride';

@Component({
  selector: 'app-ride-listings',
  templateUrl: './ride-listings.component.html',
  styleUrls: ['./ride-listings.component.css']
})
export class RideListingsComponent implements OnInit {

  parameters;
  rides: Ride[];

  constructor(
    private formService: SearchFormService,
    private searchService: SearchService) { }

  ngOnInit() {
    this.rides = [];

    // Get search results based on parameters passed from form
    this.parameters = this.formService.getSearchQuery();
    this.searchService.getRides(this.parameters['start'], this.parameters['end'],
    this.parameters['date']).subscribe(rides => {
      this.rides = rides;
      rides.forEach(ride => {
        console.log(ride);
      });
    });
  }

  getFormattedDate(date: string) {
    const formattedDate = new Date(`${date}T00:00:00`).toDateString();
    if (formattedDate === 'Invalid Date') {
      return '';
    }
    return formattedDate;
  }
}
