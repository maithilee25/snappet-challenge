import { Component, OnInit } from '@angular/core';
import * as Chartist from 'chartist';
import { HttpClient } from '@angular/common/http';

interface ProgressData {
  userId: string;
  subject: string;
  exerciseId: string;
  progress: string;
  learningObjective: string;
}

interface WorkData {
  avgProgress: number;
  submittedAssessments: number;
  submittedExercises: number;
  studentsAssessed: number;
  progressData: ProgressData[];
  subjects: string[];
  learningObjectives: string[];
}

interface ChartSeriesData {
  labels: string[];
  series: number[];
}

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  public httpClient: HttpClient;

  public progressData: ProgressData[] = [];
  public avgProgress: number;
  public submittedAssessments: number;
  public submittedExercises: number;
  public studentsAssessed: number;
  
  public learningObjectives: string[] = [];
  public subjects: string[] = [];

  public weeklyProgressLabels: string[] = [];
  public weeklyProgressSeries: number[] = [];

  public subjectProgressLabels: string[] = [];
  public subjectProgressSeries: number[] = [];


  constructor(http: HttpClient) {
    this.httpClient = http;

  }


  startAnimationForLineChart(chart) {
    let seq: any, delays: any, durations: any;
    seq = 0;
    delays = 80;
    durations = 500;

    chart.on('draw', function (data) {
      if (data.type === 'line' || data.type === 'area') {
        data.element.animate({
          d: {
            begin: 600,
            dur: 700,
            from: data.path.clone().scale(1, 0).translate(0, data.chartRect.height()).stringify(),
            to: data.path.clone().stringify(),
            easing: Chartist.Svg.Easing.easeOutQuint
          }
        });
      } else if (data.type === 'point') {
        seq++;
        data.element.animate({
          opacity: {
            begin: seq * delays,
            dur: durations,
            from: 0,
            to: 1,
            easing: 'ease'
          }
        });
      }
    });

    seq = 0;
  };
  startAnimationForBarChart(chart) {
    let seq2: any, delays2: any, durations2: any;

    seq2 = 0;
    delays2 = 80;
    durations2 = 500;
    chart.on('draw', function (data) {
      if (data.type === 'bar') {
        seq2++;
        data.element.animate({
          opacity: {
            begin: seq2 * delays2,
            dur: durations2,
            from: 0,
            to: 1,
            easing: 'ease'
          }
        });
      }
    });

    seq2 = 0;
  };
  ngOnInit() {

    this.httpClient.get<WorkData>('https://4h9jessx7i.execute-api.eu-north-1.amazonaws.com/getWorkData?date=2015-03-24').subscribe(result => {
      this.avgProgress = result.avgProgress;
      this.submittedAssessments = result.submittedAssessments;
      this.submittedExercises = result.submittedExercises;
      this.studentsAssessed = result.studentsAssessed;
      
      this.progressData = result.progressData;
      this.learningObjectives = result.learningObjectives;
      this.subjects = result.subjects;
    }, error => console.error(error));


    /* ----------==========    Progress Chart initialization For Documentation    ==========---------- */

    const optionsProgressChart: any = {
      lineSmooth: Chartist.Interpolation.cardinal({
        tension: 0
      }),
      chartPadding: { top: 0, right: 0, bottom: 0, left: 0 },
    }

    this.httpClient.get<ChartSeriesData>('https://4h9jessx7i.execute-api.eu-north-1.amazonaws.com/getWeeklyProgress?date=2015-03-24').subscribe(result => {
      this.weeklyProgressLabels = result.labels;
      this.weeklyProgressSeries = result.series;

      const dataProgressChart: any = {
        labels: this.weeklyProgressLabels,
        series: [this.weeklyProgressSeries]
      };

      var progressChart = new Chartist.Line('#progressChart', dataProgressChart, optionsProgressChart);
      this.startAnimationForLineChart(progressChart);
    }, error => console.error(error));



    /* ----------==========     Subject Progress Chart Initialization    ==========---------- */

    var optionsSubjectProgressChart = {
      axisX: {
        showGrid: true
      },
      chartPadding: { top: 0, right: 5, bottom: 0, left: 0 }
    };
    var responsiveOptions: any[] = [
      ['screen and (max-width: 640px)', {
        seriesBarDistance: 5,
        axisX: {
          labelInterpolationFnc: function (value) {
            return value[0];
          }
        }
      }]
    ];

    this.httpClient.get<ChartSeriesData>('https://4h9jessx7i.execute-api.eu-north-1.amazonaws.com/getSubjectProgress?date=2015-03-24').subscribe(result => {
      this.subjectProgressLabels = result.labels;
      this.subjectProgressSeries = result.series;

      const dataSubjectProgressChart: any = {
        labels: this.subjectProgressLabels,
        series: [this.subjectProgressSeries]
      };

      var subjectProgressChart = new Chartist.Bar('#subjectProgressChart', dataSubjectProgressChart, optionsSubjectProgressChart, responsiveOptions);
      this.startAnimationForBarChart(subjectProgressChart);
    }, error => console.error(error));

  }

}
