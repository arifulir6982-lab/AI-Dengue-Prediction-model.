import type {HistoricalRow} from './types';
export const historical:HistoricalRow[]=[
 {month:'Jan',cases:24,rainfall_mm:7,temperature_c:21,humidity_pct:67},{month:'Feb',cases:18,rainfall_mm:14,temperature_c:23,humidity_pct:64},
 {month:'Mar',cases:29,rainfall_mm:38,temperature_c:26,humidity_pct:68},{month:'Apr',cases:45,rainfall_mm:92,temperature_c:28,humidity_pct:73},
 {month:'May',cases:76,rainfall_mm:248,temperature_c:29,humidity_pct:80},{month:'Jun',cases:112,rainfall_mm:512,temperature_c:29,humidity_pct:86},
 {month:'Jul',cases:154,rainfall_mm:598,temperature_c:29,humidity_pct:88},{month:'Aug',cases:179,rainfall_mm:486,temperature_c:29,humidity_pct:87},
 {month:'Sep',cases:166,rainfall_mm:345,temperature_c:29,humidity_pct:85},{month:'Oct',cases:121,rainfall_mm:202,temperature_c:28,humidity_pct:82},
 {month:'Nov',cases:68,rainfall_mm:54,temperature_c:26,humidity_pct:76},{month:'Dec',cases:37,rainfall_mm:18,temperature_c:23,humidity_pct:70}
].map((r,i)=>({...r,predicted:Math.round(r.cases*(0.92+(i%3)*0.07))}));
export const alerts=[
 {id:'DG-104',area:'Chattogram',level:'High',date:'Next 2–4 weeks',title:'Elevated seasonal suitability',detail:'Scenario index is elevated in the demo profile.',factors:'Above-reference humidity · Monsoon rainfall'},
 {id:'DG-103',area:'Dhaka',level:'High',date:'Next 2–4 weeks',title:'Monitor local trend',detail:'Synthetic regional indicator crosses the high display band.',factors:'Seasonality · Historical demo trend'},
 {id:'DG-102',area:'Cox’s Bazar',level:'Moderate',date:'Next 2–4 weeks',title:'Routine surveillance',detail:'Moderate synthetic indicator; verify with local surveillance.',factors:'Humidity · Rainfall'}
];
