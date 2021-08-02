import React from 'react';
import { Group } from '@vx/group';
import { AxisLeft, AxisBottom } from '@vx/axis';
import { Bar } from '@vx/shape';
import { scaleTime, scaleLinear } from '@vx/scale';
import { extent } from 'd3-array';
import { timeFormat } from 'd3-time-format';

export default function Popup ({county, arrests, countyData, predictionStart, today}) {
    const width = 215;
    const height = 150;
    const margin = {
        top: 20,
        bottom: 30,
        left: 10,
        right: 10,
    };
    const xMax = width - margin.left - margin.right;
    const yMax = height - margin.top - margin.bottom;
    // Anonymous functions to extract right data from each element in countyData
    const x = d => d.x;
    const y = d => d.y;

    const xScale = scaleTime({
        range: [0, xMax],
        domain: extent(countyData, x)
    });
    const yScale = scaleLinear({
        range: [yMax, 0],
        domain: [0, Math.max(...countyData.map(y))]
    });
    const yearFormat = timeFormat('%Y');
    const formatDate = date => yearFormat(date);

    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];

    const chart = (
        <svg width={width} height={height}>
            <rect x={0} y={0} width={width} height={height} fill="#f7f7f7" rx={14} />
            <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" stopColor="#FFFFFF" stopOpacity={1} />
                    <stop offset="100%" stopColor="#FFFFFF" stopOpacity={0.2} />
                </linearGradient>
            </defs>
            <AxisLeft
                label={'Arrests'}
                top={15}
                scale={yScale}
                hideAxisLine={true}
                left={15}
                hideTicks={true}
                tickLabelProps={(value, index) => ({
                    fontSize: 7,
                    textAnchor: 'middle'
                })}
            />
            <AxisBottom
                top={yMax + margin.top}
                tickFormat={formatDate}
                scale={xScale}
                left={15}
                hideAxisLine={false}
                tickLabelProps={(value, index) => ({
                    fontSize: 7,
                    textAnchor: 'middle'
                })}
            />
            <Group top={15} left={15}>
                {countyData.map((d, i) => {
                    const year = x(d);
                    const barHeight = yMax - yScale(y(d));
                    const barX = xScale(year);
                    const barY = yMax - barHeight;
                    return (
                        <Bar
                            key={`bar-${year}`}
                            x={barX}
                            y={barY}
                            width={4}
                            height={barHeight}
                            fill={year >= Date.parse(predictionStart) ? "#c1cefa" : "#0b4fad"}
                        />
                    );
                })}
            </Group>
        </svg>
    )
    return (
        <div className="py-2 px-2">
          <strong className="popup-header my-2">
          {county}
          </strong>
          <p className='popup-body my-2'>
            <b>{arrests}</b> {today >= Date.parse(predictionStart) ? 'predicted' : null} {arrests === 1 ? 'arrest' : 'arrests'} in {monthNames[today.getMonth()]}{' '}{today.getFullYear()}
          </p>
          <p className='popup-body my-2'>
            Arrests and predictions:
          </p>
          <div className='mt-2 mr-1'>
            {chart}
          </div>
        </div>
    );
}
