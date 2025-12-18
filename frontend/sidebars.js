// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Foundations',
      items: [
        '1-introduction-to-physical-ai',
        '2-foundations-of-robotics',
        '3-sensors-perception',
        '4-actuators-control-systems'
      ],
    },
    {
      type: 'category',
      label: 'Architecture & Intelligence',
      items: [
        '5-humanoid-robot-architecture',
        '6-embodied-intelligence',
        '7-reinforcement-learning-for-robotics',
        '8-sim2real-transfer'
      ],
    },
    {
      type: 'category',
      label: 'Interaction & Future',
      items: [
        '9-human-robot-interaction',
        '10-ethical-safety-considerations',
        '11-future-of-humanoid-robotics'
      ],
    },
  ],
};

module.exports = sidebars;