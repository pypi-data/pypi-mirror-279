<a name="readme-top"></a>

[![pypi][pypi-shield]][pypi-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

# CoFFE Analyzer

> This package supports the CoFFE analysis presented in ARP4761A/ED-135.

CoFFE stands for Combinational Functional Failures Effects. One method of performing this analysis is through a table. Each row of that table represents a combination of failures leading to a certain result. 

This package analyze that table and returns a simplified boolean expression for each relevant CoFFE result (Failure Condition), that helps to develop its related preliminary Fault Tree Analysis (FTA).

## Installation

For installing CoFFE Analyzer, just run this command in your shell:

```bash
pip install coffe-analyzer
```

## Usage example

Section Q.4.4.1 of ARP4761A shows an example of a CoFFE analysis that assess the loss of ability to decelerate with crew aware. Combination of failures from four different systems are identified (Wheel Brake, Ground Spoiler, Thrust Reverser, and Flap), and three failure states are contemplated for each of them (Total Loss - F, Partal Loss - D, and Nominal Operation - O). The results after combining those failure states are: High-speed overrun, Low-speed overrun, and No overrun. Only High-speed overrun is considered relevant as Failure Condition.

Last paragraph of Section Q.4.4.1 states the solution:
> Through the CoFFE analysis it can be concluded that “the total loss of wheel brake function in addition to the partial (or total) loss of any ground spoiler or thrust reverser or flap functions” might result in high-speed overruns. 

### CSV as source of data
Considering that Table Q.4.6 is stored in a csv file, the following code is executed:

```py
>>> from coffeanalyzer import CoffeInstance

>>> path_csv = 'path/to/csv/file.csv'
>>> # The CSV wil contain one column per each analyzed system indicating the failed states.
>>> # The last column is reserved for the result of the combinated failed states:
>>> # F;F;F;F;High-speed overrun
>>> # F;O;O;O;Low-speed overrun
>>> # ...
>>> coffe = CoffeInstance(
...         ignored_states=['O'], 
...         ignored_results=['No overrun', 'Low-speed overrun'], 
...         custom_headers=['WBrake', 'GrndSpoiler', 'ThrustRev', 'Flap']
...         )
>>> coffe_results = coffe.get_simplified_expression_from_csv(path_csv)
>>> print(coffe_results)
WBrake_F AND (Flap_D OR Flap_F OR GrndSpoiler_D OR GrndSpoiler_F OR ThrustRev_D OR ThrustRev_F)
```

> [!IMPORTANT]
> The resulting boolean expression does not pretend to substitute the safety engineer to perform the FTAs. 
> 
> E.g., in this example the boolean expression can be further developed since an OR gate between a total loss and a partial loss is equal to partial loss, so the final expression to use in the corresponding FTA is:
> 
> ***WBrake_F AND (Flap_D OR GrndSpoiler_D OR ThrustRev_D)***

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Release History

* 1.0.0
    * First release

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap
- [x] Capability to obtain the boolean expression from a csv file.
- [ ] Compatibility with python4capella.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

1. Fork it (<https://github.com/samuelglorente/coffe_analyzer/fork>)
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -am 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a new Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License
Distributed under the GPL-3.0 license. See ``LICENSE`` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Samuel García Lorente

[LinkedIn](https://www.linkedin.com/in/sglorente/) – [email](sglorente@proton.me) - [GitHub](https://www.github.com/samuelglorente/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments
* [SymPy](https://github.com/sympy/sympy)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[pypi-shield]: https://img.shields.io/pypi/v/coffe-analyzer.svg?style=for-the-badge
[pypi-url]: https://pypi.python.org/pypi/coffe-analyzer
[contributors-shield]: https://img.shields.io/github/contributors/samuelglorente/coffe_analyzer.svg?style=for-the-badge
[contributors-url]: https://github.com/samuelglorente/coffe_analyzer/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/samuelglorente/coffe_analyzer.svg?style=for-the-badge
[forks-url]: https://github.com/samuelglorente/coffe_analyzer/network/members
[stars-shield]: https://img.shields.io/github/stars/samuelglorente/coffe_analyzer.svg?style=for-the-badge
[stars-url]: https://github.com/samuelglorente/coffe_analyzer/stargazers
[issues-shield]: https://img.shields.io/github/issues/samuelglorente/coffe_analyzer.svg?style=for-the-badge
[issues-url]: https://github.com/samuelglorente/coffe_analyzer/issues
[license-shield]: https://img.shields.io/github/license/samuelglorente/coffe_analyzer.svg?style=for-the-badge
[license-url]: https://github.com/samuelglorente/coffe_analyzer/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/sglorente/
[github-url]: https://www.github.com/samuelglorente/
