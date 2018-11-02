import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TripSearchComponent } from './trip-search.component';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

describe('TripSearchComponent', () => {
  let component: TripSearchComponent;
  let fixture: ComponentFixture<TripSearchComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TripSearchComponent ],
      imports: [ReactiveFormsModule, HttpClientModule]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TripSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
