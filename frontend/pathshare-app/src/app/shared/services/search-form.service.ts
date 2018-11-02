import { Injectable } from '@angular/core';

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
