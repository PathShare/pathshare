import { Injectable } from '@angular/core';


/**
 * @description passes search form information between search and listings component.
 */
@Injectable({
  providedIn: 'root'
})
export class SearchFormService {

  private formData = {start: '', end: '', date: ''};

  constructor() { }

  setSearchQuery(startLocation: string, endLocation: string, startDate: string) {
    this.formData = {start: startLocation, end: endLocation, date: startDate};
  }

  getSearchQuery() {
    return this.formData;
  }
}
