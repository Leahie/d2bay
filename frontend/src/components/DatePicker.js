import React, { useState } from 'react';
import { DayPicker } from 'react-day-picker';
import 'react-day-picker/dist/style.css';

export default function MyDatePicker() {
  const [selected, setSelected] = useState();

  return (
    <div>
      <DayPicker
        mode="single"
        selected={selected}
        onSelect={setSelected}
      />
      {selected && <p>You picked {selected.toLocaleDateString()}</p>}
    </div>
  );
}
