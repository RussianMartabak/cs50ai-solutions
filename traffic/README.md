I tried changing a lot of things including optimizer algorithm, numbers of neuron on the hidden layer, 
but nothing seem to work and there is no consistent improvement in the accuracy. However once I tried changing the size of the filter the accuracy of the neural network, there is a vast improvement of accuracy of the network. Finding how optimize the network is hard, as the results are often inconsistent, so I tested each change twice sometime even thrice. After many more experimentations I found out a configuration that can reliably produce 93% accuracy, and so I settled in that last configuration

Results = 0,0556
        = 0,0565
        = 0,0562
        = 0,0567
        = 0.2605
        = 0.1223
        = 0.0938
        = 0.1757
        = 0.0546
        = 0.0566
        = 0.0552
        = 0.0560
        = 0.0556 -> increased pooling size
        = 0.6060 -> decreased filters and increased filter size
        = 0.8967 -> increased filters
        = 0.8622 -> increased filter size
        = 0.8860
        = 0.8990
        = 0.9119
        = 0.9229
        = 0.9371
        = 0.9370
        = 0.9368 -> 115 neurons