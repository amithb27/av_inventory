import React from "react";
import {
  Tabs,
  TabsHeader,

  Tab,

} from "@material-tailwind/react";
 
export default function HomeTabs() {
  const [activeTab, setActiveTab] = React.useState(0);
  const data = [
    {
      label: "Employee List",
      value: 0,
      
    },
    {
      label: "OptionB",
      value:1,
 
    },
    {
      label: "OptionC",
      value:2,

    },
    {
      label: "OptionD",
      value:3,

    },
    {
      label: "OptionE",
      value: 4,
     
    },
    
  ];
  return (
    <Tabs value={activeTab}>
      <TabsHeader
        className="rounded-none border-b border-blue-gray-50 bg-transparent p-0"
        indicatorProps={{
          className: "bg-transparent border-b-2 border-blue-500 shadow-none rounded-none",
        }}
      >
        {data.map(({ label, value }) => (
          <Tab
            key={value}
            value={value}
            onClick={() => setActiveTab(value)}
            className={activeTab === value ? "text-blue-500" : ""}
          >
            {label}
          </Tab>
        ))}
      </TabsHeader>

    </Tabs>
  );
}
